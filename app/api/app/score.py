from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user_id
from app.schemas.score import ScoreOrderCreateRequest
from app.services import score as score_service
from app.utils.response import success

router = APIRouter(prefix="/score", tags=["积分"])


@router.get("/products")
async def get_score_products(
    page: int = Query(1),
    page_size: int = Query(10),
    db: AsyncSession = Depends(get_db),
):
    """获取积分商品列表"""
    data = await score_service.get_score_products(db, page, page_size)
    result = {
        "list": [
            {
                "id": p.id, "title": p.title, "image": p.image,
                "score": p.score, "stock": p.stock, "sales": p.sales,
            }
            for p in data["list"]
        ],
        "total": data["total"],
    }
    return success(result)


@router.get("/product/{product_id}")
async def get_score_product_detail(product_id: int, db: AsyncSession = Depends(get_db)):
    """获取积分商品详情"""
    data = await score_service.get_score_product_detail(db, product_id)
    return success(data)


@router.post("/order/create")
async def create_score_order(
    req: ScoreOrderCreateRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """积分兑换下单"""
    data = await score_service.create_score_order(
        db, uid, req.product_id, req.number,
        req.real_name, req.phone, req.address_id, req.mark, req.shop_id,
    )
    return success(data)


@router.get("/orders")
async def get_score_orders(
    status: Optional[int] = Query(None),
    page: int = Query(1),
    page_size: int = Query(10),
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取积分订单列表"""
    data = await score_service.get_score_orders(db, uid, status, page, page_size)
    result = {
        "list": [
            {
                "id": o.id, "order_id": o.order_id,
                "product_title": o.product_title, "product_image": o.product_image,
                "score": o.score, "number": o.number, "total_score": o.total_score,
                "status": o.status,
                "create_time": o.create_time.isoformat() if o.create_time else None,
            }
            for o in data["list"]
        ],
        "total": data["total"],
    }
    return success(result)
