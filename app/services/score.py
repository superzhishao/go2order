import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.score import ScoreProduct, ScoreOrder
from app.models.user import MemberUser, UserAddress


async def get_score_products(db: AsyncSession, page: int = 1, page_size: int = 10) -> dict:
    """获取积分商品列表"""
    stmt = select(ScoreProduct).where(ScoreProduct.is_switch == 1, ScoreProduct.deleted == False)
    count_stmt = select(func.count(ScoreProduct.id)).where(ScoreProduct.is_switch == 1, ScoreProduct.deleted == False)
    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(ScoreProduct.weigh.desc()).offset((page - 1) * page_size).limit(page_size)
    products = (await db.execute(stmt)).scalars().all()
    return {"list": products, "total": total}


async def get_score_product_detail(db: AsyncSession, product_id: int) -> dict:
    """获取积分商品详情"""
    stmt = select(ScoreProduct).where(ScoreProduct.id == product_id, ScoreProduct.deleted == False)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="积分商品不存在")
    return {
        "id": product.id,
        "title": product.title,
        "image": product.image,
        "images": product.images,
        "desc": product.desc,
        "score": product.score,
        "stock": product.stock,
        "sales": product.sales,
    }


async def create_score_order(db: AsyncSession, uid: int, product_id: int, number: int = 1,
                              real_name: Optional[str] = None, phone: Optional[str] = None,
                              address_id: Optional[int] = None, mark: Optional[str] = None,
                              shop_id: int = 0) -> dict:
    """积分兑换下单"""
    product = (await db.execute(
        select(ScoreProduct).where(ScoreProduct.id == product_id, ScoreProduct.deleted == False)
    )).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="积分商品不存在")
    if product.stock < number:
        raise HTTPException(status_code=400, detail="库存不足")

    total_score = product.score * number

    user = (await db.execute(select(MemberUser).where(MemberUser.id == uid))).scalar_one()
    if user.integral < total_score:
        raise HTTPException(status_code=400, detail="积分不足")

    # 获取地址
    user_address = ""
    if address_id:
        addr = (await db.execute(select(UserAddress).where(UserAddress.id == address_id))).scalar_one_or_none()
        if addr:
            real_name = real_name or addr.real_name
            phone = phone or addr.phone
            user_address = f"{addr.province or ''}{addr.city or ''}{addr.district or ''}{addr.detail or ''}"

    order_id = datetime.now().strftime("%Y%m%d%H%M%S") + "S" + uuid.uuid4().hex[:6].upper()

    order = ScoreOrder(
        uid=uid,
        order_id=order_id,
        product_id=product_id,
        product_title=product.title,
        product_image=product.image,
        score=product.score,
        number=number,
        total_score=total_score,
        real_name=real_name,
        user_phone=phone,
        user_address=user_address,
        mark=mark,
        shop_id=shop_id,
        status=0,
    )
    db.add(order)

    # 扣减积分和库存
    user.integral -= total_score
    product.stock -= number
    product.sales += number

    await db.flush()
    return {"order_id": order.order_id, "total_score": total_score}


async def get_score_orders(db: AsyncSession, uid: int, status: Optional[int] = None,
                            page: int = 1, page_size: int = 10) -> dict:
    """获取积分订单列表"""
    stmt = select(ScoreOrder).where(ScoreOrder.uid == uid, ScoreOrder.deleted == False)
    count_stmt = select(func.count(ScoreOrder.id)).where(ScoreOrder.uid == uid, ScoreOrder.deleted == False)

    if status is not None:
        stmt = stmt.where(ScoreOrder.status == status)
        count_stmt = count_stmt.where(ScoreOrder.status == status)

    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(ScoreOrder.id.desc()).offset((page - 1) * page_size).limit(page_size)
    orders = (await db.execute(stmt)).scalars().all()
    return {"list": orders, "total": total}
