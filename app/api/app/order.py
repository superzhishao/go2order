from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user_id
from app.schemas.order import (
    CreateOrderRequest, PayOrderRequest, RefundRequest, ComputeOrderRequest,
)
from app.services import order as order_service
from app.services import store as store_service
from app.utils.response import success

router = APIRouter(prefix="/order", tags=["订单"])


@router.post("/guest-create")
async def guest_create_order(
    req: CreateOrderRequest,
    db: AsyncSession = Depends(get_db),
):
    """免登录创建订单（扫码点餐）"""
    data = await order_service.create_order(db, 0, req)
    return success(data)


@router.get("/guest-query")
async def guest_query_order(
    order_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """免登录查询订单（通过订单号）"""
    data = await order_service.get_order_by_order_id(db, order_id)
    return success(data)


@router.get("/table-orders")
async def get_table_orders(
    table_no: str = Query(...),
    shop_id: int = Query(1),
    lang: Optional[str] = Query(None, description="语言代码"),
    db: AsyncSession = Depends(get_db),
):
    """根据桌号查询当日订单"""
    data = await order_service.get_table_orders(db, table_no, shop_id, lang)
    return success(data)


@router.post("/create")
async def create_order(
    req: CreateOrderRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """创建订单"""
    data = await order_service.create_order(db, uid, req)
    return success(data)


@router.post("/compute")
async def compute_order(
    req: ComputeOrderRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """计算订单价格"""
    data = await order_service.compute_order(db, uid, req)
    return success(data)


@router.post("/pay")
async def pay_order(
    req: PayOrderRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """订单支付"""
    data = await order_service.pay_order(db, uid, req.order_id, req.pay_type)
    return success(data)


@router.get("/list")
async def get_orders(
    type: int = Query(0, description="0全部 1待付款 2待发货 3待收货 4待评价 5已完成 6退款"),
    page: int = Query(1),
    limit: int = Query(10),
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取订单列表"""
    data = await order_service.get_user_orders(db, uid, type, page, limit)
    return success(data)


@router.get("/detail/{key}")
async def get_order_detail(
    key: str,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取订单详情"""
    data = await order_service.get_order_detail(db, uid, key)
    return success(data)


@router.post("/take")
async def confirm_receipt(
    uni: str,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """确认收货"""
    await order_service.confirm_receipt(db, uid, uni)
    return success(msg="收货成功")


@router.post("/refund")
async def apply_refund(
    req: RefundRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """申请退款"""
    await order_service.apply_refund(db, uid, req.order_id, req.reason, req.explain, req.images)
    return success(msg="申请成功")


@router.post("/cancel")
async def cancel_order(
    id: int,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """取消订单"""
    await order_service.cancel_order(db, uid, id)
    return success(msg="取消成功")


@router.post("/del")
async def delete_order(
    uni: str,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """删除订单"""
    await order_service.cancel_order(db, uid, int(uni) if uni.isdigit() else 0)
    return success(msg="删除成功")


@router.post("/user_count")
async def get_user_count(
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取订单统计"""
    data = await order_service.get_order_count(db, uid)
    return success(data)


@router.get("/getShop")
async def get_shop(
    shopId: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """获取门店信息"""
    data = await store_service.get_shop_detail(db, shopId)
    return success(data)
