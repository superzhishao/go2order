from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_admin_id
from app.models.score import ScoreProduct, ScoreOrder
from app.schemas.score import ScoreProductCreateRequest, ScoreProductUpdateRequest
from app.utils.response import success, page_result

router = APIRouter(prefix="/score", tags=["管理-积分"], dependencies=[Depends(get_current_admin_id)])


# ============ 积分商品 ============

@router.get("/product/list")
async def get_score_products(
    page: int = Query(1, alias="pageNo"),
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """获取积分商品列表"""
    stmt = select(ScoreProduct).where(ScoreProduct.deleted == False)
    count_stmt = select(func.count(ScoreProduct.id)).where(ScoreProduct.deleted == False)
    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(ScoreProduct.weigh.desc(), ScoreProduct.id.desc())
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    products = (await db.execute(stmt)).scalars().all()

    items = [
        {
            "id": p.id, "title": p.title, "image": p.image,
            "score": p.score, "stock": p.stock, "sales": p.sales,
            "isSwitch": p.is_switch, "weigh": p.weigh,
            "createTime": p.create_time.isoformat() if p.create_time else None,
        }
        for p in products
    ]
    return page_result(items, total, page, page_size)


@router.post("/product/create")
async def create_score_product(req: ScoreProductCreateRequest, db: AsyncSession = Depends(get_db)):
    """创建积分商品"""
    product = ScoreProduct(**req.model_dump())
    db.add(product)
    await db.flush()
    return success({"id": product.id})


@router.put("/product/update")
async def update_score_product(req: ScoreProductUpdateRequest, db: AsyncSession = Depends(get_db)):
    """更新积分商品"""
    product = (await db.execute(
        select(ScoreProduct).where(ScoreProduct.id == req.id)
    )).scalar_one_or_none()
    if not product:
        return success(None, msg="积分商品不存在")
    for field, value in req.model_dump(exclude={"id"}).items():
        setattr(product, field, value)
    await db.flush()
    return success(msg="更新成功")


@router.delete("/product/delete")
async def delete_score_product(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    """删除积分商品"""
    product = (await db.execute(select(ScoreProduct).where(ScoreProduct.id == id))).scalar_one_or_none()
    if product:
        product.deleted = True
        await db.flush()
    return success(msg="删除成功")


# ============ 积分订单 ============

@router.get("/order/list")
async def get_score_orders(
    status: Optional[int] = Query(None),
    page: int = Query(1, alias="pageNo"),
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """获取积分订单列表"""
    stmt = select(ScoreOrder).where(ScoreOrder.deleted == False)
    count_stmt = select(func.count(ScoreOrder.id)).where(ScoreOrder.deleted == False)

    if status is not None:
        stmt = stmt.where(ScoreOrder.status == status)
        count_stmt = count_stmt.where(ScoreOrder.status == status)

    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(ScoreOrder.id.desc()).offset((page - 1) * page_size).limit(page_size)
    orders = (await db.execute(stmt)).scalars().all()

    items = [
        {
            "id": o.id, "orderId": o.order_id, "uid": o.uid,
            "productTitle": o.product_title, "productImage": o.product_image,
            "score": o.score, "number": o.number, "totalScore": o.total_score,
            "realName": o.real_name, "userPhone": o.user_phone,
            "status": o.status,
            "createTime": o.create_time.isoformat() if o.create_time else None,
        }
        for o in orders
    ]
    return page_result(items, total, page, page_size)


@router.put("/order/delivery")
async def delivery_score_order(
    order_id: str, delivery_name: Optional[str] = None,
    delivery_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """积分订单发货"""
    order = (await db.execute(
        select(ScoreOrder).where(ScoreOrder.order_id == order_id)
    )).scalar_one_or_none()
    if not order:
        return success(None, msg="订单不存在")
    order.status = 1
    order.delivery_name = delivery_name
    order.delivery_id = delivery_id
    await db.flush()
    return success(msg="发货成功")
