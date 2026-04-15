from decimal import Decimal
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CouponOut(BaseModel):
    id: int
    title: str
    value: Decimal = Decimal("0")
    least: Decimal = Decimal("0")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    type: int = 0
    image: Optional[str] = None
    instructions: Optional[str] = None
    shop_name: Optional[str] = None
    receive: int = 0
    distribute: int = 0
    is_received: bool = False  # 当前用户是否已领取

    model_config = {"from_attributes": True}


class MyCouponOut(BaseModel):
    id: int
    coupon_id: int
    coupon_title: Optional[str] = None
    coupon_value: Decimal = Decimal("0")
    coupon_least: Decimal = Decimal("0")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: int = 0
    type: int = 0
    shop_id: Optional[str] = None

    model_config = {"from_attributes": True}


class ReceiveCouponRequest(BaseModel):
    id: int
    code: Optional[str] = None


# ============ Admin Schemas ============

class CouponCreateRequest(BaseModel):
    title: str
    shop_id: Optional[str] = "0"
    shop_name: Optional[str] = None
    value: Decimal = Decimal("0")
    least: Decimal = Decimal("0")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    type: int = 0
    is_switch: int = 1
    distribute: int = 0
    score: int = 0
    instructions: Optional[str] = None
    image: Optional[str] = None
    limit: int = 1
    exchange_code: Optional[str] = None


class CouponUpdateRequest(CouponCreateRequest):
    id: int
