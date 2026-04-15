from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services import product as product_service
from app.utils.response import success

router = APIRouter(prefix="/product", tags=["商品"])


@router.get("/products")
async def get_products(
    shop_id: int = Query(..., description="门店ID"),
    cate_id: Optional[int] = Query(None, description="分类ID"),
    lang: Optional[str] = Query(None, description="语言代码"),
    db: AsyncSession = Depends(get_db),
):
    """获取商品列表（按分类分组）"""
    data = await product_service.get_products_with_categories(db, shop_id, cate_id, lang)
    return success(data)


@router.get("/detail/{product_id}")
async def get_product_detail(
    product_id: int,
    lang: Optional[str] = Query(None, description="语言代码"),
    db: AsyncSession = Depends(get_db),
):
    """获取商品详情"""
    data = await product_service.get_product_detail(db, product_id, lang)
    return success(data)


@router.get("/category")
async def get_categories(
    shop_id: Optional[int] = Query(None),
    lang: Optional[str] = Query(None, description="语言代码"),
    db: AsyncSession = Depends(get_db),
):
    """获取分类列表"""
    categories = await product_service.get_categories(db, shop_id)
    data = [{"id": c.id, "name": product_service.resolve_i18n(c.name, c.name_i18n, lang), "pic_url": c.pic_url, "parent_id": c.parent_id, "sort": c.sort} for c in categories]
    return success(data)
