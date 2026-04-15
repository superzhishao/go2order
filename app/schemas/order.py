from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


# ============ App Schemas ============

class CartItem(BaseModel):
    product_id: int
    unique: Optional[str] = None  # SKU unique value
    cart_num: int = 1


class ConfirmOrderRequest(BaseModel):
    cart_items: List[CartItem]
    shop_id: int
    order_type: str = "takein"  # takein=自取, takeout=外卖


class ComputeOrderRequest(BaseModel):
    cart_items: List[CartItem]
    shop_id: int
    order_type: str = "takein"
    coupon_id: Optional[int] = None
    use_integral: bool = False
    address_id: Optional[int] = None


class CreateOrderRequest(BaseModel):
    cart_items: List[CartItem]
    shop_id: int
    order_type: str = "takein"  # takein=自取, takeout=外卖
    coupon_id: Optional[int] = None
    use_integral: bool = False
    mark: Optional[str] = None
    real_name: Optional[str] = None
    phone: Optional[str] = None
    address_id: Optional[int] = None
    pay_type: str = "weixin"  # weixin/yue
    get_time: Optional[str] = None  # 取餐时间
    table_no: Optional[str] = None  # 桌号


class PayOrderRequest(BaseModel):
    order_id: str
    pay_type: str = "weixin"
    from_type: str = "weixin"  # weixin/routine/h5


class RefundRequest(BaseModel):
    order_id: str
    reason: str
    explain: Optional[str] = None
    images: Optional[str] = None


class OrderCartInfoOut(BaseModel):
    id: int
    title: Optional[str] = None
    image: Optional[str] = None
    number: int = 1
    spec: Optional[str] = None
    price: Decimal = Decimal("0")
    product_id: int = 0

    model_config = {"from_attributes": True}


class OrderListOut(BaseModel):
    id: int
    order_id: str
    total_num: int = 0
    total_price: Decimal = Decimal("0")
    pay_price: Decimal = Decimal("0")
    paid: int = 0
    status: int = 0
    order_type: Optional[str] = None
    shop_name: Optional[str] = None
    number_id: Optional[int] = None
    create_time: Optional[datetime] = None
    cart_info: List[OrderCartInfoOut] = []

    model_config = {"from_attributes": True}


class OrderDetailOut(OrderListOut):
    real_name: Optional[str] = None
    user_phone: Optional[str] = None
    user_address: Optional[str] = None
    coupon_price: Decimal = Decimal("0")
    deduction_price: Decimal = Decimal("0")
    freight_price: Decimal = Decimal("0")
    pay_type: Optional[str] = None
    pay_time: Optional[datetime] = None
    mark: Optional[str] = None
    refund_status: int = 0
    get_time: Optional[datetime] = None
    verify_code: Optional[str] = None
    delivery_name: Optional[str] = None
    delivery_id: Optional[str] = None


class OrderCountOut(BaseModel):
    unpaid: int = 0
    unshipped: int = 0
    received: int = 0
    completed: int = 0
    refund: int = 0


class ComputeOrderResult(BaseModel):
    total_price: Decimal = Decimal("0")
    pay_price: Decimal = Decimal("0")
    coupon_price: Decimal = Decimal("0")
    deduction_price: Decimal = Decimal("0")
    freight_price: Decimal = Decimal("0")
    use_integral: Decimal = Decimal("0")


# ============ Admin Schemas ============

class OrderPageRequest(BaseModel):
    status: Optional[int] = None
    order_id: Optional[str] = None
    shop_id: Optional[int] = None
    order_type: Optional[str] = None
    page: int = 1
    page_size: int = 10


class OrderDeliveryRequest(BaseModel):
    order_id: str
    delivery_name: Optional[str] = None
    delivery_id: Optional[str] = None
    delivery_type: str = "express"


class OrderRefundRequest(BaseModel):
    order_id: str
    refund_price: Decimal
    refund_reason: Optional[str] = None
