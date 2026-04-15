import uuid
import hashlib
from datetime import datetime, timezone, date
from decimal import Decimal
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import select, func, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import StoreOrder, StoreOrderCartInfo, StoreOrderStatus, OrderNumber
from app.models.product import StoreProduct, StoreProductAttrValue
from app.models.store import StoreShop
from app.models.user import MemberUser, UserAddress
from app.models.coupon import CouponUser
from app.schemas.order import (
    CreateOrderRequest, CartItem, ComputeOrderRequest, OrderPageRequest,
)


def _generate_order_id() -> str:
    """生成订单号"""
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex[:8].upper()


async def _get_next_number(db: AsyncSession, shop_id: int) -> int:
    """获取下一个取餐号"""
    today = date.today().isoformat()
    stmt = select(OrderNumber).where(
        OrderNumber.shop_id == shop_id,
        OrderNumber.date_str == today,
    )
    result = await db.execute(stmt)
    num_obj = result.scalar_one_or_none()

    if num_obj:
        num_obj.number += 1
        await db.flush()
        return num_obj.number
    else:
        num_obj = OrderNumber(shop_id=shop_id, number=1, date_str=today)
        db.add(num_obj)
        await db.flush()
        return 1


async def compute_order(db: AsyncSession, uid: int, data: ComputeOrderRequest) -> dict:
    """计算订单价格"""
    total_price = Decimal("0")
    total_num = 0

    for item in data.cart_items:
        product = (await db.execute(
            select(StoreProduct).where(StoreProduct.id == item.product_id, StoreProduct.deleted == False)
        )).scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=400, detail=f"商品{item.product_id}不存在")

        if item.unique:
            attr_val = (await db.execute(
                select(StoreProductAttrValue).where(
                    StoreProductAttrValue.product_id == item.product_id,
                    StoreProductAttrValue.unique == item.unique,
                )
            )).scalar_one_or_none()
            price = attr_val.price if attr_val else product.price
            stock = attr_val.stock if attr_val else product.stock
        else:
            price = product.price
            stock = product.stock

        if stock < item.cart_num:
            raise HTTPException(status_code=400, detail=f"商品{product.store_name}库存不足")

        total_price += price * item.cart_num
        total_num += item.cart_num

    # 优惠券
    coupon_price = Decimal("0")
    if data.coupon_id:
        coupon_user = (await db.execute(
            select(CouponUser).where(
                CouponUser.id == data.coupon_id,
                CouponUser.uid == uid,
                CouponUser.status == 0,
            )
        )).scalar_one_or_none()
        if coupon_user and total_price >= coupon_user.coupon_least:
            coupon_price = coupon_user.coupon_value

    # 积分抵扣
    deduction_price = Decimal("0")
    if data.use_integral:
        user = (await db.execute(select(MemberUser).where(MemberUser.id == uid))).scalar_one_or_none()
        if user and user.integral > 0:
            deduction_price = min(user.integral / 100, total_price - coupon_price)

    # 配送费
    freight_price = Decimal("0")
    if data.order_type == "takeout":
        shop = (await db.execute(select(StoreShop).where(StoreShop.id == data.shop_id))).scalar_one_or_none()
        if shop:
            freight_price = shop.delivery_price

    pay_price = total_price - coupon_price - deduction_price + freight_price
    if pay_price < 0:
        pay_price = Decimal("0")

    return {
        "total_price": total_price,
        "pay_price": pay_price,
        "coupon_price": coupon_price,
        "deduction_price": deduction_price,
        "freight_price": freight_price,
        "use_integral": deduction_price * 100,
    }


async def create_order(db: AsyncSession, uid: int, data: CreateOrderRequest) -> dict:
    """创建订单"""
    # 计算价格
    compute_data = ComputeOrderRequest(
        cart_items=data.cart_items,
        shop_id=data.shop_id,
        order_type=data.order_type,
        coupon_id=data.coupon_id,
        use_integral=data.use_integral,
        address_id=data.address_id,
    )
    price_info = await compute_order(db, uid, compute_data)

    # 获取门店信息
    shop = (await db.execute(select(StoreShop).where(StoreShop.id == data.shop_id))).scalar_one_or_none()
    shop_name = shop.name if shop else ""

    # 获取取餐号
    number_id = await _get_next_number(db, data.shop_id)

    # 获取配送地址
    real_name = data.real_name or ""
    user_phone = data.phone or ""
    user_address = ""
    if data.order_type == "takeout" and data.address_id:
        addr = (await db.execute(select(UserAddress).where(UserAddress.id == data.address_id))).scalar_one_or_none()
        if addr:
            real_name = addr.real_name or real_name
            user_phone = addr.phone or user_phone
            user_address = f"{addr.province or ''}{addr.city or ''}{addr.district or ''}{addr.detail or ''}"

    order_id = _generate_order_id()
    unique = hashlib.md5(order_id.encode()).hexdigest()
    verify_code = uuid.uuid4().hex[:8].upper()

    order = StoreOrder(
        order_id=order_id,
        uid=uid,
        real_name=real_name,
        user_phone=user_phone,
        user_address=user_address,
        total_num=sum(item.cart_num for item in data.cart_items),
        total_price=price_info["total_price"],
        pay_price=price_info["pay_price"],
        coupon_id=data.coupon_id or 0,
        coupon_price=price_info["coupon_price"],
        deduction_price=price_info["deduction_price"],
        freight_price=price_info["freight_price"],
        use_integral=price_info["use_integral"],
        pay_type=data.pay_type,
        order_type=data.order_type,
        mark=data.mark,
        unique=unique,
        verify_code=verify_code,
        shop_id=data.shop_id,
        shop_name=shop_name,
        number_id=number_id,
        table_no=getattr(data, 'table_no', None),
        shipping_type=2 if data.order_type == "takein" else 1,
    )
    db.add(order)
    await db.flush()

    # 保存订单商品明细
    for item in data.cart_items:
        product = (await db.execute(
            select(StoreProduct).where(StoreProduct.id == item.product_id)
        )).scalar_one()

        spec = ""
        price = product.price
        image = product.image
        if item.unique:
            attr_val = (await db.execute(
                select(StoreProductAttrValue).where(
                    StoreProductAttrValue.product_id == item.product_id,
                    StoreProductAttrValue.unique == item.unique,
                )
            )).scalar_one_or_none()
            if attr_val:
                price = attr_val.price
                spec = attr_val.sku or ""
                if attr_val.image:
                    image = attr_val.image

        cart_info = StoreOrderCartInfo(
            oid=order.id,
            order_id=order_id,
            product_id=item.product_id,
            title=product.store_name,
            image=image,
            number=item.cart_num,
            spec=spec,
            price=price,
            unique=item.unique or "",
        )
        db.add(cart_info)

        # 扣减库存
        product.stock -= item.cart_num
        product.sales += item.cart_num
        if item.unique:
            await db.execute(
                update(StoreProductAttrValue).where(
                    StoreProductAttrValue.product_id == item.product_id,
                    StoreProductAttrValue.unique == item.unique,
                ).values(
                    stock=StoreProductAttrValue.stock - item.cart_num,
                    sales=StoreProductAttrValue.sales + item.cart_num,
                )
            )

    # 使用优惠券
    if data.coupon_id:
        await db.execute(
            update(CouponUser).where(CouponUser.id == data.coupon_id).values(
                status=1, use_time=datetime.now(timezone.utc),
            )
        )

    # 扣减积分
    if data.use_integral and price_info["use_integral"] > 0:
        await db.execute(
            update(MemberUser).where(MemberUser.id == uid).values(
                integral=MemberUser.integral - price_info["use_integral"],
            )
        )

    # 记录订单状态
    status_log = StoreOrderStatus(
        oid=order.id,
        change_type="create",
        change_message="订单创建成功",
        change_time=datetime.now(timezone.utc),
    )
    db.add(status_log)
    await db.flush()

    return {
        "order_id": order.order_id,
        "pay_price": str(order.pay_price),
        "number_id": order.number_id,
        "table_no": order.table_no,
    }


async def get_order_by_order_id(db: AsyncSession, order_id: str) -> dict:
    """通过订单号查询订单（免登录）"""
    stmt = select(StoreOrder).where(StoreOrder.order_id == order_id, StoreOrder.deleted == False)
    order = (await db.execute(stmt)).scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    cart_items = (await db.execute(
        select(StoreOrderCartInfo).where(StoreOrderCartInfo.oid == order.id)
    )).scalars().all()

    return {
        "id": order.id, "order_id": order.order_id,
        "total_num": order.total_num, "total_price": str(order.total_price),
        "pay_price": str(order.pay_price), "paid": order.paid,
        "status": order.status, "order_type": order.order_type,
        "table_no": order.table_no, "number_id": order.number_id,
        "shop_name": order.shop_name, "mark": order.mark,
        "create_time": order.create_time.isoformat() if order.create_time else None,
        "cart_info": [{"title": c.title, "image": c.image, "number": c.number,
                       "spec": c.spec, "price": str(c.price)} for c in cart_items],
    }


async def get_table_orders(db: AsyncSession, table_no: str, shop_id: int, lang: Optional[str] = None) -> list:
    """根据桌号查询当前轮次订单（结算后的新一轮）"""
    from app.models.table import StoreTable
    from app.models.product import StoreProduct
    from app.services.product import resolve_i18n

    # Find last settlement time for this table
    table = (await db.execute(
        select(StoreTable).where(
            StoreTable.table_no == table_no,
            StoreTable.shop_id == shop_id,
            StoreTable.deleted == False,
        )
    )).scalar_one_or_none()

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # Use the later of: today start OR last settled time
    cutoff = today_start
    if table and table.last_settled_at and table.last_settled_at > cutoff:
        cutoff = table.last_settled_at

    stmt = select(StoreOrder).where(
        StoreOrder.table_no == table_no,
        StoreOrder.shop_id == shop_id,
        StoreOrder.create_time > cutoff,
        StoreOrder.deleted == False,
    ).order_by(StoreOrder.id.desc())
    orders = (await db.execute(stmt)).scalars().all()

    # Collect all cart items and look up product i18n names
    all_oids = [o.id for o in orders]
    all_carts = []
    product_i18n_map = {}
    if all_oids:
        all_carts = (await db.execute(
            select(StoreOrderCartInfo).where(StoreOrderCartInfo.oid.in_(all_oids))
        )).scalars().all()

        if lang:
            product_ids = list(set(c.product_id for c in all_carts if c.product_id))
            if product_ids:
                prods = (await db.execute(
                    select(StoreProduct.id, StoreProduct.store_name, StoreProduct.store_name_i18n).where(
                        StoreProduct.id.in_(product_ids)
                    )
                )).all()
                product_i18n_map = {p.id: (p.store_name, p.store_name_i18n) for p in prods}

    carts_by_oid = {}
    for c in all_carts:
        carts_by_oid.setdefault(c.oid, []).append(c)

    result = []
    for o in orders:
        cart_items = carts_by_oid.get(o.id, [])
        result.append({
            "id": o.id, "order_id": o.order_id,
            "total_num": o.total_num, "pay_price": str(o.pay_price),
            "paid": o.paid, "status": o.status,
            "table_no": o.table_no,
            "create_time": o.create_time.isoformat() if o.create_time else None,
            "cart_info": [{"title": _resolve_cart_title(c, product_i18n_map, lang),
                           "image": c.image, "number": c.number,
                           "spec": c.spec, "price": str(c.price),
                           "cancelled": c.cancelled} for c in cart_items],
        })
    return result


def _resolve_cart_title(cart_item, product_i18n_map: dict, lang: Optional[str]) -> str:
    """Resolve cart item title using product i18n if available."""
    if lang and cart_item.product_id and cart_item.product_id in product_i18n_map:
        from app.services.product import resolve_i18n
        base, i18n_dict = product_i18n_map[cart_item.product_id]
        return resolve_i18n(base, i18n_dict, lang)
    return cart_item.title


async def pay_order(db: AsyncSession, uid: int, order_id: str, pay_type: str) -> dict:
    """订单支付"""
    stmt = select(StoreOrder).where(
        StoreOrder.order_id == order_id,
        StoreOrder.uid == uid,
        StoreOrder.deleted == False,
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.paid == 1:
        raise HTTPException(status_code=400, detail="订单已支付")

    # 余额支付
    if pay_type == "yue":
        user = (await db.execute(select(MemberUser).where(MemberUser.id == uid))).scalar_one()
        if user.now_money < order.pay_price:
            raise HTTPException(status_code=400, detail="余额不足")
        user.now_money -= order.pay_price
        user.pay_count += 1

        order.paid = 1
        order.pay_time = datetime.now(timezone.utc)
        order.pay_type = "yue"
        order.status = 0  # 待制作/待发货

        # 赠送积分
        if order.gain_integral > 0:
            user.integral += order.gain_integral

        await db.flush()
        return {"paid": True, "order_id": order.order_id}

    # 微信支付 - 返回待支付状态，前端调起支付
    # TODO: 对接微信支付
    return {"paid": False, "order_id": order.order_id, "msg": "请使用微信支付"}


async def get_user_orders(db: AsyncSession, uid: int, status_type: int = 0,
                           page: int = 1, limit: int = 10) -> dict:
    """获取用户订单列表"""
    stmt = select(StoreOrder).where(
        StoreOrder.uid == uid,
        StoreOrder.is_system_del == 0,
        StoreOrder.deleted == False,
    )
    count_stmt = select(func.count(StoreOrder.id)).where(
        StoreOrder.uid == uid,
        StoreOrder.is_system_del == 0,
        StoreOrder.deleted == False,
    )

    # status_type: 0全部 1待付款 2待发货 3待收货 4待评价 5已完成 6退款
    if status_type == 1:
        stmt = stmt.where(StoreOrder.paid == 0)
        count_stmt = count_stmt.where(StoreOrder.paid == 0)
    elif status_type == 2:
        stmt = stmt.where(StoreOrder.paid == 1, StoreOrder.status == 0)
        count_stmt = count_stmt.where(StoreOrder.paid == 1, StoreOrder.status == 0)
    elif status_type == 3:
        stmt = stmt.where(StoreOrder.paid == 1, StoreOrder.status == 1)
        count_stmt = count_stmt.where(StoreOrder.paid == 1, StoreOrder.status == 1)
    elif status_type == 4:
        stmt = stmt.where(StoreOrder.paid == 1, StoreOrder.status == 2)
        count_stmt = count_stmt.where(StoreOrder.paid == 1, StoreOrder.status == 2)
    elif status_type == 5:
        stmt = stmt.where(StoreOrder.paid == 1, StoreOrder.status == 3)
        count_stmt = count_stmt.where(StoreOrder.paid == 1, StoreOrder.status == 3)
    elif status_type == 6:
        stmt = stmt.where(StoreOrder.refund_status > 0)
        count_stmt = count_stmt.where(StoreOrder.refund_status > 0)

    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(StoreOrder.id.desc()).offset((page - 1) * limit).limit(limit)
    orders = (await db.execute(stmt)).scalars().all()

    # 获取订单商品明细
    order_list = []
    for order in orders:
        cart_stmt = select(StoreOrderCartInfo).where(StoreOrderCartInfo.oid == order.id)
        carts = (await db.execute(cart_stmt)).scalars().all()

        order_list.append({
            "id": order.id,
            "order_id": order.order_id,
            "total_num": order.total_num,
            "total_price": order.total_price,
            "pay_price": order.pay_price,
            "paid": order.paid,
            "status": order.status,
            "order_type": order.order_type,
            "shop_name": order.shop_name,
            "number_id": order.number_id,
            "create_time": order.create_time.isoformat() if order.create_time else None,
            "cart_info": [
                {
                    "id": c.id,
                    "title": c.title,
                    "image": c.image,
                    "number": c.number,
                    "spec": c.spec,
                    "price": c.price,
                    "product_id": c.product_id,
                }
                for c in carts
            ],
        })

    return {"list": order_list, "total": total}


async def get_order_detail(db: AsyncSession, uid: int, key: str) -> dict:
    """获取订单详情"""
    stmt = select(StoreOrder).where(
        StoreOrder.uid == uid,
        StoreOrder.deleted == False,
    )
    # key可以是order_id或id
    if key.isdigit():
        stmt = stmt.where(StoreOrder.id == int(key))
    else:
        stmt = stmt.where(StoreOrder.order_id == key)

    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    cart_stmt = select(StoreOrderCartInfo).where(StoreOrderCartInfo.oid == order.id)
    carts = (await db.execute(cart_stmt)).scalars().all()

    return {
        "id": order.id,
        "order_id": order.order_id,
        "total_num": order.total_num,
        "total_price": order.total_price,
        "pay_price": order.pay_price,
        "paid": order.paid,
        "status": order.status,
        "order_type": order.order_type,
        "shop_name": order.shop_name,
        "number_id": order.number_id,
        "real_name": order.real_name,
        "user_phone": order.user_phone,
        "user_address": order.user_address,
        "coupon_price": order.coupon_price,
        "deduction_price": order.deduction_price,
        "freight_price": order.freight_price,
        "pay_type": order.pay_type,
        "pay_time": order.pay_time.isoformat() if order.pay_time else None,
        "mark": order.mark,
        "refund_status": order.refund_status,
        "get_time": order.get_time.isoformat() if order.get_time else None,
        "verify_code": order.verify_code,
        "delivery_name": order.delivery_name,
        "delivery_id": order.delivery_id,
        "create_time": order.create_time.isoformat() if order.create_time else None,
        "cart_info": [
            {
                "id": c.id,
                "title": c.title,
                "image": c.image,
                "number": c.number,
                "spec": c.spec,
                "price": c.price,
                "product_id": c.product_id,
            }
            for c in carts
        ],
    }


async def cancel_order(db: AsyncSession, uid: int, order_id: int) -> None:
    """取消订单（退回库存/优惠券/积分）"""
    stmt = select(StoreOrder).where(StoreOrder.id == order_id, StoreOrder.uid == uid)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.paid == 1:
        raise HTTPException(status_code=400, detail="已支付订单无法取消")

    # 退回库存
    carts = (await db.execute(
        select(StoreOrderCartInfo).where(StoreOrderCartInfo.oid == order.id)
    )).scalars().all()

    for cart in carts:
        product = (await db.execute(
            select(StoreProduct).where(StoreProduct.id == cart.product_id)
        )).scalar_one_or_none()
        if product:
            product.stock += cart.number
            product.sales = max(0, product.sales - cart.number)

    # 退回优惠券
    if order.coupon_id:
        await db.execute(
            update(CouponUser).where(CouponUser.id == order.coupon_id).values(
                status=0, use_time=None,
            )
        )

    # 退回积分
    if order.use_integral > 0:
        await db.execute(
            update(MemberUser).where(MemberUser.id == uid).values(
                integral=MemberUser.integral + order.use_integral,
            )
        )

    order.is_system_del = 1
    order.status = -1

    status_log = StoreOrderStatus(
        oid=order.id,
        change_type="cancel",
        change_message="用户取消订单",
        change_time=datetime.now(timezone.utc),
    )
    db.add(status_log)
    await db.flush()


async def confirm_receipt(db: AsyncSession, uid: int, unique: str) -> None:
    """确认收货"""
    stmt = select(StoreOrder).where(
        StoreOrder.unique == unique,
        StoreOrder.uid == uid,
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.status != 1:
        raise HTTPException(status_code=400, detail="当前订单状态无法确认收货")

    order.status = 2
    status_log = StoreOrderStatus(
        oid=order.id,
        change_type="take",
        change_message="用户已收货",
        change_time=datetime.now(timezone.utc),
    )
    db.add(status_log)
    await db.flush()


async def apply_refund(db: AsyncSession, uid: int, order_id: str,
                       reason: str, explain: Optional[str] = None,
                       images: Optional[str] = None) -> None:
    """申请退款"""
    stmt = select(StoreOrder).where(StoreOrder.order_id == order_id, StoreOrder.uid == uid)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    order.refund_status = 1
    order.refund_reason_wap = reason
    order.refund_reason_wap_explain = explain
    order.refund_reason_wap_img = images
    order.refund_reason_time = datetime.now(timezone.utc)
    order.status = -1

    status_log = StoreOrderStatus(
        oid=order.id,
        change_type="refund_apply",
        change_message=f"用户申请退款: {reason}",
        change_time=datetime.now(timezone.utc),
    )
    db.add(status_log)
    await db.flush()


async def get_order_count(db: AsyncSession, uid: int) -> dict:
    """获取用户订单统计"""
    base = and_(StoreOrder.uid == uid, StoreOrder.is_system_del == 0, StoreOrder.deleted == False)

    unpaid = (await db.execute(select(func.count(StoreOrder.id)).where(base, StoreOrder.paid == 0))).scalar()
    unshipped = (await db.execute(select(func.count(StoreOrder.id)).where(base, StoreOrder.paid == 1, StoreOrder.status == 0))).scalar()
    received = (await db.execute(select(func.count(StoreOrder.id)).where(base, StoreOrder.paid == 1, StoreOrder.status == 2))).scalar()
    completed = (await db.execute(select(func.count(StoreOrder.id)).where(base, StoreOrder.paid == 1, StoreOrder.status == 3))).scalar()
    refund = (await db.execute(select(func.count(StoreOrder.id)).where(base, StoreOrder.refund_status > 0))).scalar()

    return {
        "unpaid": unpaid,
        "unshipped": unshipped,
        "received": received,
        "completed": completed,
        "refund": refund,
    }
