from decimal import Decimal
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ScoreProductOut(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    score: int = 0
    stock: int = 0
    sales: int = 0

    model_config = {"from_attributes": True}


class ScoreProductDetailOut(ScoreProductOut):
    images: Optional[list] = None
    desc: Optional[str] = None


class ScoreOrderCreateRequest(BaseModel):
    product_id: int
    number: int = 1
    real_name: Optional[str] = None
    phone: Optional[str] = None
    address_id: Optional[int] = None
    mark: Optional[str] = None
    shop_id: int = 0


class ScoreOrderOut(BaseModel):
    id: int
    order_id: str
    product_title: Optional[str] = None
    product_image: Optional[str] = None
    score: int = 0
    number: int = 1
    total_score: int = 0
    status: int = 0
    create_time: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ============ Admin Schemas ============

class ScoreProductCreateRequest(BaseModel):
    title: str
    image: Optional[str] = None
    images: Optional[list] = None
    desc: Optional[str] = None
    score: int = 0
    stock: int = 0
    weigh: int = 0
    is_switch: int = 1


class ScoreProductUpdateRequest(ScoreProductCreateRequest):
    id: int
