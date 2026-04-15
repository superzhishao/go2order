from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel


class StoreShopOut(BaseModel):
    id: int
    name: str
    mobile: Optional[str] = None
    image: Optional[str] = None
    address: Optional[str] = None
    lng: Optional[str] = None
    lat: Optional[str] = None
    distance_km: Optional[float] = None  # computed distance
    min_price: Decimal = Decimal("0")
    delivery_price: Decimal = Decimal("0")
    notice: Optional[str] = None
    status: int = 1
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    model_config = {"from_attributes": True}


class StoreShopDetailOut(StoreShopOut):
    images: Optional[list] = None
    address_map: Optional[str] = None
    uniprint_id: Optional[str] = None


class NearbyRequest(BaseModel):
    lng: Optional[str] = None
    lat: Optional[str] = None
    kw: Optional[str] = None
    shop_id: Optional[int] = None


# ============ Admin Schemas ============

class StoreShopCreateRequest(BaseModel):
    name: str
    mobile: Optional[str] = None
    image: Optional[str] = None
    images: Optional[list] = None
    address: Optional[str] = None
    address_map: Optional[str] = None
    lng: Optional[str] = None
    lat: Optional[str] = None
    distance: int = 0
    min_price: Decimal = Decimal("0")
    delivery_price: Decimal = Decimal("0")
    notice: Optional[str] = None
    status: int = 1
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class StoreShopUpdateRequest(StoreShopCreateRequest):
    id: int
