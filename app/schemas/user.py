from decimal import Decimal
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserProfileOut(BaseModel):
    id: int
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    mobile: Optional[str] = None
    now_money: Decimal = Decimal("0")
    integral: Decimal = Decimal("0")
    level: int = 0
    pay_count: int = 0
    coupon_count: int = 0
    order_count: int = 0

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    birthday: Optional[str] = None
    real_name: Optional[str] = None


class AddressCreateRequest(BaseModel):
    real_name: str
    phone: str
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    detail: str
    is_default: bool = False
    lng: Optional[str] = None
    lat: Optional[str] = None


class AddressUpdateRequest(AddressCreateRequest):
    id: int


class AddressOut(BaseModel):
    id: int
    real_name: Optional[str] = None
    phone: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    detail: Optional[str] = None
    is_default: bool = False

    model_config = {"from_attributes": True}


# ============ Admin Schemas ============

class MemberUserPageRequest(BaseModel):
    nickname: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[int] = None
    page: int = 1
    page_size: int = 10


class MemberUserOut(BaseModel):
    id: int
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    mobile: Optional[str] = None
    now_money: Decimal = Decimal("0")
    integral: Decimal = Decimal("0")
    level: int = 0
    status: int = 0
    pay_count: int = 0
    create_time: Optional[datetime] = None
    login_date: Optional[datetime] = None

    model_config = {"from_attributes": True}
