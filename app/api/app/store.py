from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.store import StoreShop
from app.services import store as store_service
from app.utils.response import success

router = APIRouter(prefix="/store", tags=["门店"])


@router.get("/nearby")
async def get_nearby(
    lng: Optional[str] = Query(None),
    lat: Optional[str] = Query(None),
    kw: Optional[str] = Query(None),
    shop_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取最近门店"""
    data = await store_service.get_nearby_store(db, lng, lat, kw, shop_id)
    return success(data)


@router.get("/list")
async def get_store_list(
    lng: Optional[str] = Query(None),
    lat: Optional[str] = Query(None),
    kw: Optional[str] = Query(None),
    shop_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取门店列表"""
    data = await store_service.get_store_list(db, lng, lat, kw, shop_id)
    return success(data)


@router.get("/getShop")
async def get_shop(
    shop_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """获取门店详情"""
    data = await store_service.get_shop_detail(db, shop_id)
    return success(data)


@router.get("/theme")
async def get_shop_theme(
    shop_id: int = Query(1),
    db: AsyncSession = Depends(get_db),
):
    """获取店铺主题（Logo+色调，无需登录）"""
    shop = (await db.execute(
        select(StoreShop).where(StoreShop.id == shop_id, StoreShop.deleted == False)
    )).scalar_one_or_none()
    if not shop:
        return success({"name": "", "logo": None, "themeColor": None, "currency": "¥", "enabledLanguages": [], "defaultLanguage": "zh"})
    return success({
        "name": shop.name,
        "logo": shop.logo,
        "themeColor": shop.theme_color,
        "currency": shop.currency or "¥",
        "notice": shop.notice,
        "noticeI18n": shop.notice_i18n,
        "enabledLanguages": shop.enabled_languages or [],
        "defaultLanguage": shop.default_language or "zh",
    })
