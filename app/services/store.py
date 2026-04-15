import math
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import StoreShop
from app.schemas.store import StoreShopCreateRequest, StoreShopUpdateRequest


def _calc_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """计算两点距离（千米）- Haversine公式"""
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


async def get_nearby_store(db: AsyncSession, lng: Optional[str] = None, lat: Optional[str] = None,
                            kw: Optional[str] = None, shop_id: Optional[int] = None) -> Optional[dict]:
    """获取最近的门店"""
    stores = await get_store_list(db, lng, lat, kw, shop_id)
    return stores[0] if stores else None


async def get_store_list(db: AsyncSession, lng: Optional[str] = None, lat: Optional[str] = None,
                          kw: Optional[str] = None, shop_id: Optional[int] = None) -> list:
    """获取门店列表"""
    stmt = select(StoreShop).where(StoreShop.deleted == False, StoreShop.status == 1)

    if shop_id:
        stmt = stmt.where(StoreShop.id == shop_id)
    if kw:
        stmt = stmt.where(StoreShop.name.contains(kw))

    result = await db.execute(stmt)
    shops = result.scalars().all()

    shop_list = []
    for shop in shops:
        distance_km = None
        if lng and lat and shop.lng and shop.lat:
            try:
                distance_km = round(_calc_distance(
                    float(lat), float(lng),
                    float(shop.lat), float(shop.lng),
                ), 2)
            except (ValueError, TypeError):
                pass

        shop_list.append({
            "id": shop.id,
            "name": shop.name,
            "mobile": shop.mobile,
            "image": shop.image,
            "address": shop.address,
            "lng": shop.lng,
            "lat": shop.lat,
            "distance_km": distance_km,
            "min_price": shop.min_price,
            "delivery_price": shop.delivery_price,
            "notice": shop.notice,
            "status": shop.status,
            "start_time": shop.start_time,
            "end_time": shop.end_time,
        })

    # 按距离排序
    if lng and lat:
        shop_list.sort(key=lambda x: x["distance_km"] if x["distance_km"] is not None else float("inf"))

    return shop_list


async def get_shop_detail(db: AsyncSession, shop_id: int) -> dict:
    """获取门店详情"""
    stmt = select(StoreShop).where(StoreShop.id == shop_id, StoreShop.deleted == False)
    result = await db.execute(stmt)
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="门店不存在")

    return {
        "id": shop.id,
        "name": shop.name,
        "mobile": shop.mobile,
        "image": shop.image,
        "images": shop.images,
        "address": shop.address,
        "address_map": shop.address_map,
        "lng": shop.lng,
        "lat": shop.lat,
        "distance": shop.distance,
        "min_price": shop.min_price,
        "delivery_price": shop.delivery_price,
        "notice": shop.notice,
        "status": shop.status,
        "start_time": shop.start_time,
        "end_time": shop.end_time,
    }


# ============ Admin ============

async def admin_get_shops(db: AsyncSession, page: int = 1, page_size: int = 10) -> dict:
    stmt = select(StoreShop).where(StoreShop.deleted == False)
    count_stmt = select(func.count(StoreShop.id)).where(StoreShop.deleted == False)
    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(StoreShop.id.desc()).offset((page - 1) * page_size).limit(page_size)
    shops = (await db.execute(stmt)).scalars().all()
    return {"list": shops, "total": total}


async def admin_create_shop(db: AsyncSession, data: StoreShopCreateRequest) -> int:
    shop = StoreShop(**data.model_dump())
    db.add(shop)
    await db.flush()
    return shop.id


async def admin_update_shop(db: AsyncSession, data: StoreShopUpdateRequest) -> None:
    stmt = select(StoreShop).where(StoreShop.id == data.id)
    result = await db.execute(stmt)
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="门店不存在")
    for field, value in data.model_dump(exclude={"id"}).items():
        setattr(shop, field, value)
    await db.flush()


async def admin_delete_shop(db: AsyncSession, shop_id: int) -> None:
    stmt = select(StoreShop).where(StoreShop.id == shop_id)
    result = await db.execute(stmt)
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="门店不存在")
    shop.deleted = True
    await db.flush()
