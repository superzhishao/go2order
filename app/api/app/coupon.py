from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user_id, get_current_user_id_optional
from app.schemas.coupon import ReceiveCouponRequest
from app.services import coupon as coupon_service
from app.utils.response import success

router = APIRouter(prefix="/coupon", tags=["优惠券"])


@router.get("/count")
async def get_coupon_count(
    shop_id: Optional[int] = Query(None),
    type: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取可用优惠券数量"""
    count = await coupon_service.get_coupon_count(db, shop_id, type)
    return success(count)


@router.get("/not")
async def get_available_coupons(
    id: Optional[int] = Query(None, description="shopId"),
    page: int = Query(1),
    pagesize: int = Query(10),
    uid: Optional[int] = Depends(get_current_user_id_optional),
    db: AsyncSession = Depends(get_db),
):
    """获取未领取的优惠券"""
    data = await coupon_service.get_available_coupons(db, id, None, uid, page, pagesize)
    return success(data)


@router.get("/my")
async def get_my_coupons(
    shopId: Optional[int] = Query(None),
    type: int = Query(0, description="0未使用 1已使用 2已过期"),
    page: int = Query(1),
    pagesize: int = Query(10),
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取我的优惠券"""
    coupons = await coupon_service.get_my_coupons(db, uid, shopId, type, page, pagesize)
    data = [
        {
            "id": c.id,
            "coupon_id": c.coupon_id,
            "coupon_title": c.coupon_title,
            "coupon_value": c.coupon_value,
            "coupon_least": c.coupon_least,
            "start_time": c.start_time.isoformat() if c.start_time else None,
            "end_time": c.end_time.isoformat() if c.end_time else None,
            "status": c.status,
            "type": c.type,
            "shop_id": c.shop_id,
        }
        for c in coupons
    ]
    return success(data)


@router.post("/receive")
async def receive_coupon(
    req: ReceiveCouponRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """领取优惠券"""
    await coupon_service.receive_coupon(db, uid, req.id, req.code)
    return success(msg="领取成功")
