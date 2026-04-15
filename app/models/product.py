from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Integer, BigInteger, DECIMAL, Text, Boolean, SmallInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import BaseMixin


class ProductCategory(BaseMixin, Base):
    """商品分类表"""
    __tablename__ = "go2run_store_product_category"

    shop_id: Mapped[int] = mapped_column(Integer, default=0, comment="店铺id")
    shop_name: Mapped[Optional[str]] = mapped_column(String(255), comment="店铺名称")
    parent_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="父分类编号")
    name: Mapped[str] = mapped_column(String(100), comment="分类名称")
    name_i18n: Mapped[Optional[dict]] = mapped_column(JSON, comment="分类名称多语言")
    pic_url: Mapped[Optional[str]] = mapped_column(String(500), comment="分类图片")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="分类排序")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="分类描述")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="开启状态")


class StoreProduct(BaseMixin, Base):
    """商品表"""
    __tablename__ = "go2run_store_product"

    shop_id: Mapped[int] = mapped_column(Integer, default=0, comment="店铺id")
    shop_name: Mapped[Optional[str]] = mapped_column(String(255), comment="店铺名称")
    image: Mapped[Optional[str]] = mapped_column(String(500), comment="商品图片")
    slider_image: Mapped[Optional[str]] = mapped_column(Text, comment="轮播图")
    store_name: Mapped[str] = mapped_column(String(255), comment="商品名称")
    store_name_i18n: Mapped[Optional[dict]] = mapped_column(JSON, comment="商品名称多语言")
    store_info: Mapped[Optional[str]] = mapped_column(String(500), comment="商品简介")
    store_info_i18n: Mapped[Optional[dict]] = mapped_column(JSON, comment="商品简介多语言")
    keyword: Mapped[Optional[str]] = mapped_column(String(255), comment="关键字")
    bar_code: Mapped[Optional[str]] = mapped_column(String(100), comment="产品条码")
    cate_id: Mapped[Optional[str]] = mapped_column(String(255), comment="分类id")
    brand_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="品牌id")
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="商品价格")
    vip_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="会员价格")
    ot_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="市场价")
    postage: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="邮费")
    unit_name: Mapped[Optional[str]] = mapped_column(String(50), comment="单位名")
    sort: Mapped[int] = mapped_column(SmallInteger, default=0, comment="排序")
    sales: Mapped[int] = mapped_column(Integer, default=0, comment="销量")
    stock: Mapped[int] = mapped_column(Integer, default=0, comment="库存")
    is_show: Mapped[int] = mapped_column(Integer, default=1, comment="状态(0未上架,1上架)")
    is_hot: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否热卖")
    is_benefit: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否优惠")
    is_best: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否精品")
    is_new: Mapped[int] = mapped_column(Integer, default=0, comment="是否新品")
    description: Mapped[Optional[str]] = mapped_column(Text, comment="产品描述")
    description_i18n: Mapped[Optional[dict]] = mapped_column(JSON, comment="产品描述多语言")
    is_postage: Mapped[int] = mapped_column(Integer, default=0, comment="是否包邮")
    give_integral: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="获得积分")
    cost: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="成本价")
    is_good: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否优品推荐")
    ficti: Mapped[int] = mapped_column(Integer, default=0, comment="虚拟销量")
    browse: Mapped[int] = mapped_column(Integer, default=0, comment="浏览量")
    is_sub: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否单独分佣")
    temp_id: Mapped[int] = mapped_column(Integer, default=0, comment="运费模板ID")
    spec_type: Mapped[int] = mapped_column(Integer, default=0, comment="规格 0单 1多")
    is_integral: Mapped[int] = mapped_column(Integer, default=0, comment="是否开启积分兑换")
    integral: Mapped[int] = mapped_column(Integer, default=0, comment="需要多少积分兑换")


class StoreProductAttr(BaseMixin, Base):
    """商品属性表"""
    __tablename__ = "go2run_store_product_attr"

    product_id: Mapped[int] = mapped_column(BigInteger, index=True, comment="商品ID")
    attr_name: Mapped[Optional[str]] = mapped_column(String(255), comment="属性名")
    attr_values: Mapped[Optional[str]] = mapped_column(Text, comment="属性值")


class StoreProductAttrValue(Base):
    """商品属性值表"""
    __tablename__ = "go2run_store_product_attr_value"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, index=True, comment="商品ID")
    sku: Mapped[Optional[str]] = mapped_column(String(255), comment="商品属性索引值")
    stock: Mapped[int] = mapped_column(Integer, default=0, comment="属性对应的库存")
    sales: Mapped[int] = mapped_column(Integer, default=0, comment="销量")
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="属性金额")
    image: Mapped[Optional[str]] = mapped_column(String(500), comment="图片")
    unique: Mapped[Optional[str]] = mapped_column("unique", String(100), comment="唯一值")
    cost: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="成本价")
    bar_code: Mapped[Optional[str]] = mapped_column(String(100), comment="商品条码")
    ot_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="原价")
    weight: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="重量")
    volume: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="体积")
    integral: Mapped[int] = mapped_column(Integer, default=0, comment="需要多少积分兑换")


class StoreProductAttrResult(Base):
    """商品属性详情表"""
    __tablename__ = "go2run_store_product_attr_result"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, index=True, comment="商品ID")
    result: Mapped[Optional[str]] = mapped_column(Text, comment="商品属性参数")
    change_time: Mapped[Optional[int]] = mapped_column(Integer, comment="变动时间")


class StoreProductRule(BaseMixin, Base):
    """商品规格表"""
    __tablename__ = "go2run_store_product_rule"

    rule_name: Mapped[str] = mapped_column(String(255), comment="规格名称")
    rule_value: Mapped[Optional[str]] = mapped_column(Text, comment="规格值")


class StoreProductReply(BaseMixin, Base):
    """商品评论表"""
    __tablename__ = "go2run_store_product_reply"

    uid: Mapped[int] = mapped_column(BigInteger, comment="用户id")
    oid: Mapped[int] = mapped_column(BigInteger, comment="订单id")
    product_id: Mapped[int] = mapped_column(BigInteger, index=True, comment="商品id")
    product_score: Mapped[int] = mapped_column(Integer, default=5, comment="商品分数")
    service_score: Mapped[int] = mapped_column(Integer, default=5, comment="服务分数")
    comment: Mapped[Optional[str]] = mapped_column(Text, comment="评论内容")
    pics: Mapped[Optional[str]] = mapped_column(Text, comment="评论图片")
    merchant_reply_content: Mapped[Optional[str]] = mapped_column(Text, comment="管理员回复内容")
    is_reply: Mapped[int] = mapped_column(Integer, default=0, comment="0未回复1已回复")
