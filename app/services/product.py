import json
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import (
    ProductCategory, StoreProduct, StoreProductAttr,
    StoreProductAttrValue, StoreProductAttrResult, StoreProductRule,
)
from app.schemas.product import (
    ProductQueryParam, ProductCreateRequest, ProductUpdateRequest,
    CategoryCreateRequest, CategoryUpdateRequest,
)


def resolve_i18n(base: str, i18n_dict: Optional[dict], lang: Optional[str]) -> str:
    """Resolve i18n value: return translated name if available, otherwise base name."""
    if lang and i18n_dict and isinstance(i18n_dict, dict):
        return i18n_dict.get(lang) or base
    return base


# ============ App Services ============

async def get_products_with_categories(db: AsyncSession, shop_id: int, cate_id: Optional[int] = None, lang: Optional[str] = None) -> list:
    """获取商品列表（按分类分组）"""
    # 获取分类
    cat_stmt = select(ProductCategory).where(
        ProductCategory.shop_id == shop_id,
        ProductCategory.status == 0,
        ProductCategory.deleted == False,
    ).order_by(ProductCategory.sort.desc())

    if cate_id:
        cat_stmt = cat_stmt.where(ProductCategory.id == cate_id)

    cat_result = await db.execute(cat_stmt)
    categories = cat_result.scalars().all()

    result = []
    for cat in categories:
        # 获取该分类下的商品
        prod_stmt = select(StoreProduct).where(
            StoreProduct.shop_id == shop_id,
            StoreProduct.is_show == 1,
            StoreProduct.deleted == False,
            func.find_in_set(str(cat.id), StoreProduct.cate_id),
        ).order_by(StoreProduct.sort.desc())

        prod_result = await db.execute(prod_stmt)
        products = prod_result.scalars().all()

        result.append({
            "id": cat.id,
            "name": resolve_i18n(cat.name, cat.name_i18n, lang),
            "pic_url": cat.pic_url,
            "products": [
                {
                    "id": p.id,
                    "image": p.image,
                    "store_name": resolve_i18n(p.store_name, p.store_name_i18n, lang),
                    "store_info": resolve_i18n(p.store_info or '', p.store_info_i18n, lang),
                    "price": p.price,
                    "ot_price": p.ot_price,
                    "sales": p.sales + p.ficti,
                    "stock": p.stock,
                    "unit_name": p.unit_name,
                    "is_show": p.is_show,
                }
                for p in products
            ],
        })

    return result


async def get_product_detail(db: AsyncSession, product_id: int, lang: Optional[str] = None) -> dict:
    """获取商品详情"""
    stmt = select(StoreProduct).where(StoreProduct.id == product_id, StoreProduct.deleted == False)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    # 增加浏览量
    product.browse = (product.browse or 0) + 1
    await db.flush()

    # 获取属性
    attr_stmt = select(StoreProductAttr).where(StoreProductAttr.product_id == product_id)
    attr_result = await db.execute(attr_stmt)
    attrs = attr_result.scalars().all()

    # 获取属性值（SKU）
    value_stmt = select(StoreProductAttrValue).where(StoreProductAttrValue.product_id == product_id)
    value_result = await db.execute(value_stmt)
    attr_values = value_result.scalars().all()

    return {
        "id": product.id,
        "shop_id": product.shop_id,
        "image": product.image,
        "slider_image": product.slider_image,
        "store_name": resolve_i18n(product.store_name, product.store_name_i18n, lang),
        "store_info": resolve_i18n(product.store_info or '', product.store_info_i18n, lang),
        "price": product.price,
        "ot_price": product.ot_price,
        "vip_price": product.vip_price,
        "stock": product.stock,
        "sales": product.sales + product.ficti,
        "unit_name": product.unit_name,
        "description": resolve_i18n(product.description or '', product.description_i18n, lang),
        "spec_type": product.spec_type,
        "give_integral": product.give_integral,
        "attrs": [{"attr_name": a.attr_name, "attr_values": a.attr_values} for a in attrs],
        "attr_values": [
            {
                "id": v.id,
                "sku": v.sku,
                "stock": v.stock,
                "price": v.price,
                "image": v.image,
                "unique": v.unique,
                "cost": v.cost,
                "ot_price": v.ot_price,
            }
            for v in attr_values
        ],
    }


# ============ Admin Services ============

async def admin_get_products(db: AsyncSession, shop_id: Optional[int] = None,
                              keyword: Optional[str] = None, page: int = 1, page_size: int = 10) -> dict:
    """管理后台获取商品列表"""
    stmt = select(StoreProduct).where(StoreProduct.deleted == False)
    count_stmt = select(func.count(StoreProduct.id)).where(StoreProduct.deleted == False)

    if shop_id is not None:
        stmt = stmt.where(StoreProduct.shop_id == shop_id)
        count_stmt = count_stmt.where(StoreProduct.shop_id == shop_id)
    if keyword:
        stmt = stmt.where(StoreProduct.store_name.contains(keyword))
        count_stmt = count_stmt.where(StoreProduct.store_name.contains(keyword))

    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(StoreProduct.sort.desc(), StoreProduct.id.desc())
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    products = (await db.execute(stmt)).scalars().all()

    return {"list": products, "total": total}


async def admin_create_product(db: AsyncSession, data: ProductCreateRequest) -> int:
    """管理后台创建商品"""
    product = StoreProduct(
        shop_id=data.shop_id,
        store_name=data.store_name,
        store_name_i18n=data.store_name_i18n,
        store_info=data.store_info,
        store_info_i18n=data.store_info_i18n,
        cate_id=data.cate_id,
        image=data.image,
        slider_image=data.slider_image,
        price=data.price,
        ot_price=data.ot_price,
        vip_price=data.vip_price,
        cost=data.cost,
        stock=data.stock,
        unit_name=data.unit_name,
        sort=data.sort,
        is_show=data.is_show,
        is_hot=data.is_hot,
        is_best=data.is_best,
        is_new=data.is_new,
        is_good=data.is_good,
        description=data.description,
        description_i18n=data.description_i18n,
        spec_type=data.spec_type,
        give_integral=data.give_integral,
        is_postage=data.is_postage,
        postage=data.postage,
        temp_id=data.temp_id,
    )
    db.add(product)
    await db.flush()

    # 保存SKU属性
    if data.attrs:
        for attr_data in data.attrs:
            attr = StoreProductAttr(
                product_id=product.id,
                attr_name=attr_data.get("attr_name", ""),
                attr_values=attr_data.get("attr_values", ""),
            )
            db.add(attr)

    if data.attr_values:
        for val_data in data.attr_values:
            val = StoreProductAttrValue(
                product_id=product.id,
                sku=val_data.get("sku", ""),
                stock=val_data.get("stock", 0),
                price=val_data.get("price", 0),
                image=val_data.get("image", ""),
                cost=val_data.get("cost", 0),
                ot_price=val_data.get("ot_price", 0),
                bar_code=val_data.get("bar_code", ""),
                unique=val_data.get("unique", ""),
            )
            db.add(val)

    # 保存属性结果
    attr_result = StoreProductAttrResult(
        product_id=product.id,
        result=json.dumps(data.attr_values) if data.attr_values else "{}",
    )
    db.add(attr_result)

    await db.flush()
    return product.id


async def admin_update_product(db: AsyncSession, data: ProductUpdateRequest) -> None:
    """管理后台更新商品"""
    stmt = select(StoreProduct).where(StoreProduct.id == data.id, StoreProduct.deleted == False)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    for field in ["store_name", "store_name_i18n", "store_info", "store_info_i18n",
                  "cate_id", "image", "slider_image",
                  "price", "ot_price", "vip_price", "cost", "stock", "unit_name",
                  "sort", "is_show", "is_hot", "is_best", "is_new", "is_good",
                  "description", "description_i18n", "spec_type", "give_integral", "is_postage", "postage"]:
        setattr(product, field, getattr(data, field))

    await db.flush()


async def admin_delete_product(db: AsyncSession, product_id: int) -> None:
    """管理后台删除商品（软删除）"""
    stmt = select(StoreProduct).where(StoreProduct.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    product.deleted = True
    await db.flush()


# ============ Category Services ============

async def get_categories(db: AsyncSession, shop_id: Optional[int] = None) -> list:
    """获取分类列表"""
    stmt = select(ProductCategory).where(ProductCategory.deleted == False, ProductCategory.status == 0)
    if shop_id is not None:
        stmt = stmt.where(ProductCategory.shop_id == shop_id)
    stmt = stmt.order_by(ProductCategory.sort.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def admin_create_category(db: AsyncSession, data: CategoryCreateRequest) -> int:
    cat = ProductCategory(
        name=data.name,
        name_i18n=data.name_i18n,
        parent_id=data.parent_id,
        pic_url=data.pic_url,
        sort=data.sort,
        status=data.status,
        shop_id=data.shop_id,
        description=data.description,
    )
    db.add(cat)
    await db.flush()
    return cat.id


async def admin_update_category(db: AsyncSession, data: CategoryUpdateRequest) -> None:
    stmt = select(ProductCategory).where(ProductCategory.id == data.id)
    result = await db.execute(stmt)
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    for field in ["name", "name_i18n", "parent_id", "pic_url", "sort", "status", "description"]:
        setattr(cat, field, getattr(data, field))
    await db.flush()


async def admin_delete_category(db: AsyncSession, category_id: int) -> None:
    stmt = select(ProductCategory).where(ProductCategory.id == category_id)
    result = await db.execute(stmt)
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    cat.deleted = True
    await db.flush()
