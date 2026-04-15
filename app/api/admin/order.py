from typing import Optional
from decimal import Decimal
from collections import OrderedDict, defaultdict

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, func, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_admin_id
from app.models.order import StoreOrder, StoreOrderCartInfo, StoreOrderStatus
from app.models.product import StoreProduct, StoreProductAttrValue
from app.models.table import StoreTable
from app.utils.response import success

from datetime import datetime, timezone, date, timedelta

router = APIRouter(prefix="/order", tags=["管理-订单"], dependencies=[Depends(get_current_admin_id)])


def _parse_date_range(date_start: Optional[str], date_end: Optional[str]):
    """Parse date_start/date_end strings (YYYY-MM-DD) into datetime range."""
    if date_start:
        ds = datetime.strptime(date_start, "%Y-%m-%d")
    else:
        ds = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if date_end:
        de = datetime.strptime(date_end, "%Y-%m-%d") + timedelta(days=1)
    else:
        de = ds + timedelta(days=1)
    return ds, de


@router.get("/table-list")
async def get_table_orders(
    shop_id: int = Query(1, alias="shopId"),
    status: Optional[str] = Query(None),
    table_no: Optional[str] = Query(None, alias="tableNo"),
    date_start: Optional[str] = Query(None, alias="dateStart"),
    date_end: Optional[str] = Query(None, alias="dateEnd"),
    db: AsyncSession = Depends(get_db),
):
    """按桌号+轮次聚合的订单列表"""
    ds, de = _parse_date_range(date_start, date_end)

    # Get all tables
    tables_stmt = select(StoreTable).where(
        StoreTable.shop_id == shop_id, StoreTable.deleted == False
    )
    all_tables = {t.table_no: t for t in (await db.execute(tables_stmt)).scalars().all()}

    # Get orders in date range
    stmt = select(StoreOrder).where(
        StoreOrder.deleted == False,
        StoreOrder.shop_id == shop_id,
        StoreOrder.create_time >= ds,
        StoreOrder.create_time < de,
        StoreOrder.table_no.isnot(None),
        StoreOrder.table_no != '',
    )
    if table_no:
        stmt = stmt.where(StoreOrder.table_no.contains(table_no))
    stmt = stmt.order_by(StoreOrder.id.asc())
    all_orders = (await db.execute(stmt)).scalars().all()

    # Group orders by (table_no, date) then split into current vs settled
    # key = (table_no, date_str)
    by_table_date = defaultdict(lambda: {"current": [], "settled": []})
    today_str = datetime.now().strftime("%Y-%m-%d")
    for o in all_orders:
        tn = o.table_no
        d = o.create_time.strftime("%Y-%m-%d") if o.create_time else today_str
        tbl = all_tables.get(tn)
        if tbl and tbl.last_settled_at and o.create_time and o.create_time <= tbl.last_settled_at:
            by_table_date[(tn, d)]["settled"].append(o)
        else:
            by_table_date[(tn, d)]["current"].append(o)

    # --- Helper: build one group ---
    def _make_group(tn, order_list, round_num, is_settled, day_str):
        g = {
            "tableNo": tn,
            "shopId": order_list[0].shop_id if order_list else shop_id,
            "round": round_num, "date": day_str,
            "orderIds": [], "items": [],
            "totalPrice": Decimal("0"), "orderCount": 0,
            "status": "settled" if is_settled else "active",
            "firstTime": None, "lastTime": None,
        }
        for o in order_list:
            g["orderIds"].append(o.id)
            g["orderCount"] += 1
            g["totalPrice"] += o.pay_price
            ts = o.create_time.isoformat() if o.create_time else None
            if g["firstTime"] is None or (ts and ts < g["firstTime"]):
                g["firstTime"] = ts
            if g["lastTime"] is None or (ts and ts > g["lastTime"]):
                g["lastTime"] = ts
        return g

    # --- Split settled orders into rounds by pay_time ---
    def _split_rounds(orders):
        """Group orders into rounds by pay_time (truncated to second)."""
        rounds = OrderedDict()
        for o in orders:
            if o.pay_time:
                key = o.pay_time.replace(microsecond=0)
            else:
                key = datetime.min
            if key not in rounds:
                rounds[key] = []
            rounds[key].append(o)
        return [orders for _, orders in sorted(rounds.items())]

    # --- Build all groups ---
    result = []
    for (tn, day_str) in sorted(by_table_date.keys()):
        data = by_table_date[(tn, day_str)]
        round_num = 1
        # Settled rounds first (chronological)
        if data["settled"]:
            rounds = _split_rounds(data["settled"])
            for round_orders in rounds:
                result.append(_make_group(tn, round_orders, round_num, True, day_str))
                round_num += 1
        # Current active session
        if data["current"]:
            result.append(_make_group(tn, data["current"], round_num, False, day_str))

    # Fill cart items for all groups
    all_oids = [oid for g in result for oid in g["orderIds"]]
    if all_oids:
        carts = (await db.execute(
            select(StoreOrderCartInfo).where(StoreOrderCartInfo.oid.in_(all_oids))
        )).scalars().all()

        # Look up product i18n names for all cart items
        product_ids = list(set(ci.product_id for ci in carts if ci.product_id))
        product_i18n_map = {}
        if product_ids:
            products = (await db.execute(
                select(StoreProduct.id, StoreProduct.store_name_i18n).where(
                    StoreProduct.id.in_(product_ids)
                )
            )).all()
            product_i18n_map = {p.id: p.store_name_i18n for p in products}

        # Map oid -> group index
        oid_to_idx = {}
        for idx, g in enumerate(result):
            for oid in g["orderIds"]:
                oid_to_idx[oid] = idx
        for ci in carts:
            idx = oid_to_idx.get(ci.oid)
            if idx is not None:
                result[idx]["items"].append({
                    "id": ci.id, "title": ci.title, "image": ci.image,
                    "number": ci.number, "spec": ci.spec,
                    "price": str(ci.price), "cancelled": ci.cancelled,
                    "orderId": ci.order_id,
                    "productId": ci.product_id,
                    "titleI18n": product_i18n_map.get(ci.product_id),
                })

    # Finalize
    for g in result:
        g["totalPrice"] = str(g["totalPrice"])

    # Filter by status
    if status == "active":
        result = [g for g in result if g["status"] == "active"]
    elif status == "settled":
        result = [g for g in result if g["status"] == "settled"]

    # Active first, then settled (newest first within each)
    active = [g for g in result if g["status"] == "active"]
    settled = [g for g in result if g["status"] == "settled"]
    settled.reverse()  # newest round first
    result = active + settled

    return success(result)


class CancelItemRequest(BaseModel):
    cart_item_id: int
    reason: Optional[str] = None


@router.put("/cancel-item")
async def cancel_item(req: CancelItemRequest, db: AsyncSession = Depends(get_db)):
    """取消单个菜品"""
    ci = (await db.execute(
        select(StoreOrderCartInfo).where(StoreOrderCartInfo.id == req.cart_item_id)
    )).scalar_one_or_none()
    if not ci:
        return success(None, msg="菜品不存在")

    ci.cancelled = 1

    # Restore stock
    product = (await db.execute(
        select(StoreProduct).where(StoreProduct.id == ci.product_id)
    )).scalar_one_or_none()
    if product:
        product.stock += ci.number
        product.sales = max(0, product.sales - ci.number)

    if ci.unique:
        await db.execute(
            update(StoreProductAttrValue).where(
                StoreProductAttrValue.product_id == ci.product_id,
                StoreProductAttrValue.unique == ci.unique,
            ).values(
                stock=StoreProductAttrValue.stock + ci.number,
                sales=func.greatest(StoreProductAttrValue.sales - ci.number, 0),
            )
        )

    # Update order total
    order = (await db.execute(
        select(StoreOrder).where(StoreOrder.id == ci.oid)
    )).scalar_one_or_none()
    if order:
        refund_amount = ci.price * ci.number
        order.pay_price = max(Decimal("0"), order.pay_price - refund_amount)
        order.total_price = max(Decimal("0"), order.total_price - refund_amount)
        order.total_num = max(0, order.total_num - ci.number)

    # Log
    db.add(StoreOrderStatus(
        oid=ci.oid, change_type="cancel_item",
        change_message=f"退单: {ci.title} x{ci.number}" + (f" 原因: {req.reason}" if req.reason else ""),
        change_time=datetime.now(timezone.utc),
    ))
    await db.flush()
    return success(msg=f"已退单: {ci.title}")


class SettleTableRequest(BaseModel):
    table_no: str
    shop_id: int = 1


@router.put("/settle-table")
async def settle_table(req: SettleTableRequest, db: AsyncSession = Depends(get_db)):
    """结算整桌"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    orders = (await db.execute(
        select(StoreOrder).where(
            StoreOrder.table_no == req.table_no,
            StoreOrder.shop_id == req.shop_id,
            StoreOrder.create_time >= today_start,
            StoreOrder.deleted == False,
            StoreOrder.status < 3,
        )
    )).scalars().all()

    if not orders:
        return success(msg="没有需要结算的订单")

    now = datetime.now(timezone.utc)
    total = Decimal("0")
    for o in orders:
        o.status = 3
        o.paid = 1
        o.pay_time = now
        total += o.pay_price
        db.add(StoreOrderStatus(
            oid=o.id, change_type="settle",
            change_message="整桌结算",
            change_time=now,
        ))

    # Update table's last_settled_at
    table = (await db.execute(
        select(StoreTable).where(
            StoreTable.table_no == req.table_no,
            StoreTable.shop_id == req.shop_id,
            StoreTable.deleted == False,
        )
    )).scalar_one_or_none()
    if table:
        table.last_settled_at = datetime.now()

    await db.flush()
    return success({"total": str(total), "count": len(orders)}, msg=f"结算成功，共¥{total}")


@router.get("/stats")
async def get_order_stats(
    shop_id: int = Query(1, alias="shopId"),
    date_start: Optional[str] = Query(None, alias="dateStart"),
    date_end: Optional[str] = Query(None, alias="dateEnd"),
    db: AsyncSession = Depends(get_db),
):
    """订单统计（支持日期范围）"""
    ds, de = _parse_date_range(date_start, date_end)

    base = and_(
        StoreOrder.deleted == False,
        StoreOrder.shop_id == shop_id,
        StoreOrder.create_time >= ds,
        StoreOrder.create_time < de,
    )

    # Order count & revenue in one query
    row = (await db.execute(
        select(
            func.count(StoreOrder.id),
            func.coalesce(func.sum(StoreOrder.pay_price), 0),
        ).where(base)
    )).one()
    order_count = row[0]
    total_revenue = row[1]

    # Paid revenue
    paid_revenue = (await db.execute(
        select(func.coalesce(func.sum(StoreOrder.pay_price), 0)).where(
            base, StoreOrder.paid == 1
        )
    )).scalar()

    # Table count
    table_count = (await db.execute(
        select(func.count(StoreTable.id)).where(
            StoreTable.shop_id == shop_id, StoreTable.deleted == False
        )
    )).scalar()

    # Total orders (all time)
    total_all = (await db.execute(
        select(func.count(StoreOrder.id)).where(
            StoreOrder.deleted == False, StoreOrder.shop_id == shop_id
        )
    )).scalar()

    return success({
        "orderCount": order_count,
        "revenue": str(paid_revenue),
        "totalRevenue": str(total_revenue),
        "tableCount": table_count,
        "totalOrders": total_all,
        "dateStart": ds.strftime("%Y-%m-%d"),
        "dateEnd": (de - timedelta(days=1)).strftime("%Y-%m-%d"),
    })


@router.get("/list")
async def get_orders(
    status: Optional[int] = Query(None),
    order_id: Optional[str] = Query(None, alias="orderId"),
    shop_id: Optional[int] = Query(None, alias="shopId"),
    date_start: Optional[str] = Query(None, alias="dateStart"),
    date_end: Optional[str] = Query(None, alias="dateEnd"),
    page: int = Query(1, alias="pageNo"),
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """获取订单列表"""
    stmt = select(StoreOrder).where(StoreOrder.deleted == False)
    count_stmt = select(func.count(StoreOrder.id)).where(StoreOrder.deleted == False)

    if date_start or date_end:
        ds, de = _parse_date_range(date_start, date_end)
        stmt = stmt.where(StoreOrder.create_time >= ds, StoreOrder.create_time < de)
        count_stmt = count_stmt.where(StoreOrder.create_time >= ds, StoreOrder.create_time < de)

    if status is not None:
        stmt = stmt.where(StoreOrder.status == status)
        count_stmt = count_stmt.where(StoreOrder.status == status)
    if order_id:
        stmt = stmt.where(StoreOrder.order_id.contains(order_id))
        count_stmt = count_stmt.where(StoreOrder.order_id.contains(order_id))
    if shop_id is not None:
        stmt = stmt.where(StoreOrder.shop_id == shop_id)
        count_stmt = count_stmt.where(StoreOrder.shop_id == shop_id)

    total = (await db.execute(count_stmt)).scalar()
    stmt = stmt.order_by(StoreOrder.id.desc()).offset((page - 1) * page_size).limit(page_size)
    orders = (await db.execute(stmt)).scalars().all()

    # Collect all order IDs and fetch cart info in batch
    order_ids = [o.id for o in orders]
    all_carts = []
    if order_ids:
        all_carts = (await db.execute(
            select(StoreOrderCartInfo).where(StoreOrderCartInfo.oid.in_(order_ids))
        )).scalars().all()

    # Look up product i18n names
    product_ids = list(set(c.product_id for c in all_carts if c.product_id))
    product_i18n_map = {}
    if product_ids:
        prods = (await db.execute(
            select(StoreProduct.id, StoreProduct.store_name_i18n).where(
                StoreProduct.id.in_(product_ids)
            )
        )).all()
        product_i18n_map = {p.id: p.store_name_i18n for p in prods}

    # Group carts by oid
    carts_by_oid = defaultdict(list)
    for c in all_carts:
        carts_by_oid[c.oid].append(c)

    items = []
    for o in orders:
        carts = carts_by_oid.get(o.id, [])
        items.append({
            "id": o.id, "orderId": o.order_id, "tableNo": o.table_no,
            "totalNum": o.total_num, "totalPrice": str(o.total_price),
            "payPrice": str(o.pay_price), "paid": o.paid, "status": o.status,
            "shopName": o.shop_name, "mark": o.mark,
            "createTime": o.create_time.isoformat() if o.create_time else None,
            "cartInfo": [
                {"id": c.id, "title": c.title, "number": c.number, "spec": c.spec,
                 "price": str(c.price), "cancelled": c.cancelled,
                 "productId": c.product_id,
                 "titleI18n": product_i18n_map.get(c.product_id)}
                for c in carts
            ],
        })
    from app.utils.response import page_result
    return page_result(items, total, page, page_size)
