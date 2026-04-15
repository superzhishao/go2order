from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import MemberUser, UserAddress
from app.models.coupon import CouponUser
from app.models.order import StoreOrder


async def get_user_profile(db: AsyncSession, uid: int) -> dict:
    """获取用户信息"""
    user = (await db.execute(
        select(MemberUser).where(MemberUser.id == uid, MemberUser.deleted == False)
    )).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 统计优惠券数量
    coupon_count = (await db.execute(
        select(func.count(CouponUser.id)).where(CouponUser.uid == uid, CouponUser.status == 0)
    )).scalar()

    # 统计订单数量
    order_count = (await db.execute(
        select(func.count(StoreOrder.id)).where(StoreOrder.uid == uid, StoreOrder.deleted == False)
    )).scalar()

    return {
        "id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "mobile": user.mobile,
        "now_money": user.now_money,
        "integral": user.integral,
        "level": user.level,
        "pay_count": user.pay_count,
        "coupon_count": coupon_count,
        "order_count": order_count,
    }


async def update_user_profile(db: AsyncSession, uid: int, nickname: Optional[str] = None,
                               avatar: Optional[str] = None, birthday: Optional[str] = None,
                               real_name: Optional[str] = None) -> None:
    """更新用户信息"""
    user = (await db.execute(select(MemberUser).where(MemberUser.id == uid))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if nickname is not None:
        user.nickname = nickname
    if avatar is not None:
        user.avatar = avatar
    if birthday is not None:
        user.birthday = birthday
    if real_name is not None:
        user.real_name = real_name
    await db.flush()


# ============ Address ============

async def get_user_addresses(db: AsyncSession, uid: int) -> list:
    """获取用户地址列表"""
    stmt = select(UserAddress).where(UserAddress.uid == uid, UserAddress.deleted == False)
    stmt = stmt.order_by(UserAddress.is_default.desc(), UserAddress.id.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_address(db: AsyncSession, uid: int, data: dict) -> int:
    """创建地址"""
    # 如果设为默认，先取消其他默认
    if data.get("is_default"):
        await db.execute(
            update(UserAddress).where(
                UserAddress.uid == uid, UserAddress.is_default == True
            ).values(is_default=False)
        )

    addr = UserAddress(uid=uid, **data)
    db.add(addr)
    await db.flush()
    return addr.id


async def update_address(db: AsyncSession, uid: int, addr_id: int, data: dict) -> None:
    """更新地址"""
    addr = (await db.execute(
        select(UserAddress).where(UserAddress.id == addr_id, UserAddress.uid == uid)
    )).scalar_one_or_none()
    if not addr:
        raise HTTPException(status_code=404, detail="地址不存在")

    if data.get("is_default"):
        await db.execute(
            update(UserAddress).where(
                UserAddress.uid == uid, UserAddress.is_default == True
            ).values(is_default=False)
        )

    for key, value in data.items():
        setattr(addr, key, value)
    await db.flush()


async def delete_address(db: AsyncSession, uid: int, addr_id: int) -> None:
    """删除地址"""
    addr = (await db.execute(
        select(UserAddress).where(UserAddress.id == addr_id, UserAddress.uid == uid)
    )).scalar_one_or_none()
    if not addr:
        raise HTTPException(status_code=404, detail="地址不存在")
    addr.deleted = True
    await db.flush()
