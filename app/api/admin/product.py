from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_admin_id
from app.schemas.product import (
    ProductCreateRequest, ProductUpdateRequest,
    CategoryCreateRequest, CategoryUpdateRequest,
)
from app.services import product as product_service
from app.utils.response import success, page_result

router = APIRouter(prefix="/product", tags=["管理-商品"], dependencies=[Depends(get_current_admin_id)])


@router.get("/list")
async def get_products(
    shop_id: Optional[int] = Query(None),
    keyword: Optional[str] = Query(None),
    page: int = Query(1, alias="pageNo"),
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """获取商品列表"""
    data = await product_service.admin_get_products(db, shop_id, keyword, page, page_size)
    items = [
        {
            "id": p.id, "shopId": p.shop_id, "storeName": p.store_name,
            "storeNameI18n": p.store_name_i18n,
            "image": p.image, "price": p.price, "stock": p.stock,
            "sales": p.sales, "isShow": p.is_show, "sort": p.sort,
            "cateId": p.cate_id, "otPrice": p.ot_price,
            "description": p.description, "descriptionI18n": p.description_i18n,
            "storeInfo": p.store_info, "storeInfoI18n": p.store_info_i18n,
            "createTime": p.create_time.isoformat() if p.create_time else None,
        }
        for p in data["list"]
    ]
    return page_result(items, data["total"], page, page_size)


@router.post("/create")
async def create_product(req: ProductCreateRequest, db: AsyncSession = Depends(get_db)):
    """创建商品"""
    product_id = await product_service.admin_create_product(db, req)
    return success({"id": product_id})


@router.put("/update")
async def update_product(req: ProductUpdateRequest, db: AsyncSession = Depends(get_db)):
    """更新商品"""
    await product_service.admin_update_product(db, req)
    return success(msg="更新成功")


@router.delete("/delete")
async def delete_product(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    """删除商品"""
    await product_service.admin_delete_product(db, id)
    return success(msg="删除成功")


# ============ 分类管理 ============

@router.get("/category/list")
async def get_categories(
    shop_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取分类列表"""
    categories = await product_service.get_categories(db, shop_id)
    data = [
        {
            "id": c.id, "name": c.name, "nameI18n": c.name_i18n,
            "picUrl": c.pic_url,
            "parentId": c.parent_id, "sort": c.sort, "status": c.status,
        }
        for c in categories
    ]
    return success(data)


@router.post("/category/create")
async def create_category(req: CategoryCreateRequest, db: AsyncSession = Depends(get_db)):
    """创建分类"""
    cat_id = await product_service.admin_create_category(db, req)
    return success({"id": cat_id})


@router.put("/category/update")
async def update_category(req: CategoryUpdateRequest, db: AsyncSession = Depends(get_db)):
    """更新分类"""
    await product_service.admin_update_category(db, req)
    return success(msg="更新成功")


@router.delete("/category/delete")
async def delete_category(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    """删除分类"""
    await product_service.admin_delete_category(db, id)
    return success(msg="删除成功")
