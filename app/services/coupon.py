from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.coupon import Coupon, CouponUser


async def get_available_coupons(db: AsyncSession, shop_id: Optional[int] = None,
                                 coupon_type: Optional[int] = None,
                                 uid: Optional[int] = None,
                                 page: int = 1, page_size: int = 10) -> list:
    """获取可领取的优惠券"""
    now = datetime.now(timezone.utc)
    stmt = select(Coupon).where(
        Coupon.is_switch == 1,
        Coupon.deleted == False,
        Coupon.start_time <= now,
        Coupon.end_time >= now,
    )

    if shop_id:
        stmt = stmt.where(
            (Coupon.shop_id == "0") | (func.find_in_set(str(shop_id), Coupon.shop_id))
        )
    if coupon_type is not None:
        stmt = stmt.where(Coupon.type == coupon_type)

    stmt = stmt.order_by(Coupon.weigh.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    coupons = result.scalars().all()

    coupon_list = []
    for coupon in coupons:
        is_received = False
        if uid:
            cnt = (await db.execute(
                select(func.count(CouponUser.id)).where(
                    CouponUser.uid == uid,
                    CouponUser.coupon_id == coupon.id,
                )
            )).scalar()
            is_received = cnt >= coupon.limit

        coupon_list.append({
            "id": coupon.id,
            "title": coupon.title,
            "value": coupon.value,
            "least": coupon.least,
            "start_time": coupon.start_time,
            "end_time": coupon.end_time,
            "type": coupon.type,
            "image": coupon.image,
            "instructions": coupon.instructions,
            "shop_name": coupon.shop_name,
            "receive": coupon.receive,
            "distribute": coupon.distribute,
            "is_received": is_received,
        })

    return coupon_list


async def get_coupon_count(db: AsyncSession, shop_id: Optional[int] = None,
                            coupon_type: Optional[int] = None) -> int:
    """获取可用优惠券数量"""
    now = datetime.now(timezone.utc)
    stmt = select(func.count(Coupon.id)).where(
        Coupon.is_switch == 1,
        Coupon.deleted == False,
        Coupon.start_time <= now,
        Coupon.end_time >= now,
    )
    if shop_id:
        stmt = stmt.where(
            (Coupon.shop_id == "0") | (func.find_in_set(str(shop_id), Coupon.shop_id))
        )
    if coupon_type is not None:
        stmt = stmt.where(Coupon.type == coupon_type)
    return (await db.execute(stmt)).scalar()


async def get_my_coupons(db: AsyncSession, uid: int, shop_id: Optional[int] = None,
                          status: int = 0, page: int = 1, page_size: int = 10) -> list:
    """获取我的优惠券"""
    now = datetime.now(timezone.utc)
    stmt = select(CouponUser).where(CouponUser.uid == uid)

    if status == 0:
        stmt = stmt.where(CouponUser.status == 0, CouponUser.end_time >= now)
    elif status == 1:
        stmt = stmt.where(CouponUser.status == 1)
    elif status == 2:
        stmt = stmt.where((CouponUser.status == 2) | (CouponUser.end_time < now))

    if shop_id:
        stmt = stmt.where(
            (CouponUser.shop_id == "0") | (CouponUser.shop_id == None) |
            (func.find_in_set(str(shop_id), CouponUser.shop_id))
        )

    stmt = stmt.order_by(CouponUser.id.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    return result.scalars().all()


async def receive_coupon(db: AsyncSession, uid: int, coupon_id: int, code: Optional[str] = None) -> None:
    """领取优惠券"""
    stmt = select(Coupon).where(Coupon.id == coupon_id, Coupon.deleted == False)
    result = await db.execute(stmt)
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=404, detail="优惠券不存在")

    now = datetime.now(timezone.utc)
    if coupon.is_switch != 1:
        raise HTTPException(status_code=400, detail="优惠券已下架")
    if coupon.start_time and coupon.start_time > now:
        raise HTTPException(status_code=400, detail="优惠券活动未开始")
    if coupon.end_time and coupon.end_time < now:
        raise HTTPException(status_code=400, detail="优惠券已过期")

    # 检查发行量
    if coupon.distribute > 0 and coupon.receive >= coupon.distribute:
        raise HTTPException(status_code=400, detail="优惠券已领完")

    # 检查限领
    cnt = (await db.execute(
        select(func.count(CouponUser.id)).where(
            CouponUser.uid == uid,
            CouponUser.coupon_id == coupon_id,
        )
    )).scalar()
    if cnt >= coupon.limit:
        raise HTTPException(status_code=400, detail="已达领取上限")

    # 兑换码
    if coupon.exchange_code and coupon.exchange_code != code:
        raise HTTPException(status_code=400, detail="兑换码错误")

    # 领取
    coupon_user = CouponUser(
        uid=uid,
        coupon_id=coupon_id,
        coupon_title=coupon.title,
        coupon_value=coupon.value,
        coupon_least=coupon.least,
        start_time=coupon.start_time,
        end_time=coupon.end_time,
        status=0,
        shop_id=coupon.shop_id,
        type=coupon.type,
    )
    db.add(coupon_user)

    coupon.receive = (coupon.receive or 0) + 1
    await db.flush()
