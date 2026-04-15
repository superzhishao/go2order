from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_admin_id
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreateRequest, CouponUpdateRequest
from app.utils.response import success, page_result

router = APIRouter(prefix="/coupon", tags=["管理-优惠券"], dependencies=[Depends(get_current_admin_id)])


@router.get("/list")
async def get_coupons(
    title: Optional[str] = Query(None),
    page: int = Query(1, alias="pageNo"),
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """获取优惠券列表"""
    stmt = select(Coupon).where(Coupon.deleted == False)
    count_stmt = select(func.count(Coupon.id)).where(Coupon.deleted == False)

    if title:
        stmt = stmt.where(Coupon.title.contains(title))
        count_stmt = count_stmt.where(Coupon.title.contains(title))

    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(Coupon.weigh.desc(), Coupon.id.desc()).offset((page - 1) * page_size).limit(page_size)
    coupons = (await db.execute(stmt)).scalars().all()

    items = [
        {
            "id": c.id, "title": c.title, "value": str(c.value), "least": str(c.least),
            "startTime": c.start_time.isoformat() if c.start_time else None,
            "endTime": c.end_time.isoformat() if c.end_time else None,
            "type": c.type, "isSwitch": c.is_switch,
            "receive": c.receive, "distribute": c.distribute,
            "createTime": c.create_time.isoformat() if c.create_time else None,
        }
        for c in coupons
    ]
    return page_result(items, total, page, page_size)


@router.post("/create")
async def create_coupon(req: CouponCreateRequest, db: AsyncSession = Depends(get_db)):
    """创建优惠券"""
    coupon = Coupon(**req.model_dump())
    db.add(coupon)
    await db.flush()
    return success({"id": coupon.id})


@router.put("/update")
async def update_coupon(req: CouponUpdateRequest, db: AsyncSession = Depends(get_db)):
    """更新优惠券"""
    stmt = select(Coupon).where(Coupon.id == req.id)
    coupon = (await db.execute(stmt)).scalar_one_or_none()
    if not coupon:
        return success(None, msg="优惠券不存在")
    for field, value in req.model_dump(exclude={"id"}).items():
        setattr(coupon, field, value)
    await db.flush()
    return success(msg="更新成功")


@router.delete("/delete")
async def delete_coupon(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    """删除优惠券"""
    stmt = select(Coupon).where(Coupon.id == id)
    coupon = (await db.execute(stmt)).scalar_one_or_none()
    if coupon:
        coupon.deleted = True
        await db.flush()
    return success(msg="删除成功")
