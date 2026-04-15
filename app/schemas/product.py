from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


# ============ App Schemas ============

class ProductQueryParam(BaseModel):
    """商品查询参数"""
    shop_id: Optional[int] = None
    cate_id: Optional[int] = None
    keyword: Optional[str] = None
    price_order: Optional[str] = None  # asc/desc
    sales_order: Optional[str] = None
    page: int = 1
    page_size: int = 10


class ProductAttrValueOut(BaseModel):
    id: int
    sku: Optional[str] = None
    stock: int = 0
    price: Decimal = Decimal("0")
    image: Optional[str] = None
    unique: Optional[str] = None
    cost: Decimal = Decimal("0")
    ot_price: Decimal = Decimal("0")

    model_config = {"from_attributes": True}


class ProductAttrOut(BaseModel):
    attr_name: Optional[str] = None
    attr_values: Optional[str] = None

    model_config = {"from_attributes": True}


class ProductListOut(BaseModel):
    id: int
    image: Optional[str] = None
    store_name: str
    price: Decimal
    ot_price: Decimal = Decimal("0")
    sales: int = 0
    stock: int = 0
    unit_name: Optional[str] = None
    is_show: int = 1

    model_config = {"from_attributes": True}


class ProductDetailOut(BaseModel):
    id: int
    shop_id: int = 0
    image: Optional[str] = None
    slider_image: Optional[str] = None
    store_name: str
    store_info: Optional[str] = None
    price: Decimal
    ot_price: Decimal = Decimal("0")
    vip_price: Decimal = Decimal("0")
    stock: int = 0
    sales: int = 0
    unit_name: Optional[str] = None
    description: Optional[str] = None
    spec_type: int = 0
    give_integral: Decimal = Decimal("0")
    attrs: List[ProductAttrOut] = []
    attr_values: List[ProductAttrValueOut] = []

    model_config = {"from_attributes": True}


class CategoryOut(BaseModel):
    id: int
    name: str
    pic_url: Optional[str] = None
    parent_id: int = 0
    sort: int = 0

    model_config = {"from_attributes": True}


class CategoryWithProducts(BaseModel):
    id: int
    name: str
    pic_url: Optional[str] = None
    products: List[ProductListOut] = []


# ============ Admin Schemas ============

class ProductCreateRequest(BaseModel):
    shop_id: int = 0
    store_name: str
    store_name_i18n: Optional[dict] = None
    store_info: Optional[str] = None
    store_info_i18n: Optional[dict] = None
    cate_id: Optional[str | int] = None
    image: Optional[str] = None
    slider_image: Optional[str] = None
    price: Decimal = Decimal("0")
    ot_price: Decimal = Decimal("0")
    vip_price: Decimal = Decimal("0")
    cost: Decimal = Decimal("0")
    stock: int = 0
    unit_name: Optional[str] = None
    sort: int = 0
    is_show: int = 1
    is_hot: bool = False
    is_best: bool = False
    is_new: int = 0
    is_good: bool = False
    description: Optional[str] = None
    description_i18n: Optional[dict] = None
    spec_type: int = 0
    give_integral: Decimal = Decimal("0")
    is_postage: int = 0
    postage: Decimal = Decimal("0")
    temp_id: int = 0
    attrs: Optional[List[dict]] = None
    attr_values: Optional[List[dict]] = None

    model_config = {"populate_by_name": True}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    def __init__(self, **data):
        # Support camelCase from frontend
        mapped = {}
        aliases = {
            'storeName': 'store_name', 'storeNameI18n': 'store_name_i18n',
            'storeInfo': 'store_info', 'storeInfoI18n': 'store_info_i18n', 'cateId': 'cate_id',
            'categoryId': 'cate_id', 'sliderImage': 'slider_image', 'otPrice': 'ot_price',
            'vipPrice': 'vip_price', 'unitName': 'unit_name', 'isShow': 'is_show',
            'isHot': 'is_hot', 'isBest': 'is_best', 'isNew': 'is_new', 'isGood': 'is_good',
            'descriptionI18n': 'description_i18n',
            'specType': 'spec_type', 'giveIntegral': 'give_integral', 'isPostage': 'is_postage',
            'tempId': 'temp_id', 'attrValues': 'attr_values', 'shopId': 'shop_id',
        }
        for k, v in data.items():
            mapped[aliases.get(k, k)] = v
        super().__init__(**mapped)


class ProductUpdateRequest(ProductCreateRequest):
    id: int


class CategoryCreateRequest(BaseModel):
    name: str
    name_i18n: Optional[dict] = None
    parent_id: int = 0
    pic_url: Optional[str] = None
    sort: int = 0
    status: int = 0
    shop_id: int = 0
    description: Optional[str] = None


class CategoryUpdateRequest(CategoryCreateRequest):
    id: int
