from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_admin_id
from app.models.user import MemberUser
from app.utils.response import success, page_result

router = APIRouter(prefix="/member/user", tags=["管理-会员"], dependencies=[Depends(get_current_admin_id)])


@router.get("/list")
async def get_users(
    nickname: Optional[str] = Query(None),
    mobile: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    page: int = Query(1, alias="pageNo"),
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """获取会员列表"""
    stmt = select(MemberUser).where(MemberUser.deleted == False)
    count_stmt = select(func.count(MemberUser.id)).where(MemberUser.deleted == False)

    if nickname:
        stmt = stmt.where(MemberUser.nickname.contains(nickname))
        count_stmt = count_stmt.where(MemberUser.nickname.contains(nickname))
    if mobile:
        stmt = stmt.where(MemberUser.mobile.contains(mobile))
        count_stmt = count_stmt.where(MemberUser.mobile.contains(mobile))
    if status is not None:
        stmt = stmt.where(MemberUser.status == status)
        count_stmt = count_stmt.where(MemberUser.status == status)

    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(MemberUser.id.desc()).offset((page - 1) * page_size).limit(page_size)
    users = (await db.execute(stmt)).scalars().all()

    items = [
        {
            "id": u.id, "nickname": u.nickname, "avatar": u.avatar,
            "mobile": u.mobile, "nowMoney": str(u.now_money),
            "integral": str(u.integral), "level": u.level, "status": u.status,
            "payCount": u.pay_count,
            "createTime": u.create_time.isoformat() if u.create_time else None,
            "loginDate": u.login_date.isoformat() if u.login_date else None,
        }
        for u in users
    ]
    return page_result(items, total, page, page_size)


@router.get("/detail/{user_id}")
async def get_user_detail(user_id: int, db: AsyncSession = Depends(get_db)):
    """获取会员详情"""
    user = (await db.execute(
        select(MemberUser).where(MemberUser.id == user_id)
    )).scalar_one_or_none()
    if not user:
        return success(None, msg="用户不存在")

    return success({
        "id": user.id, "nickname": user.nickname, "avatar": user.avatar,
        "mobile": user.mobile, "realName": user.real_name,
        "nowMoney": str(user.now_money), "integral": str(user.integral),
        "level": user.level, "status": user.status,
        "payCount": user.pay_count, "spreadCount": user.spread_count,
        "createTime": user.create_time.isoformat() if user.create_time else None,
    })


@router.put("/update-status")
async def update_user_status(
    user_id: int, status: int,
    db: AsyncSession = Depends(get_db),
):
    """更新会员状态"""
    user = (await db.execute(
        select(MemberUser).where(MemberUser.id == user_id)
    )).scalar_one_or_none()
    if user:
        user.status = status
        await db.flush()
    return success(msg="更新成功")
