from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Integer, BigInteger, DECIMAL, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import BaseMixin


class ScoreProduct(BaseMixin, Base):
    """积分产品表"""
    __tablename__ = "go2run_score_product"

    title: Mapped[str] = mapped_column(String(255), comment="产品标题")
    image: Mapped[Optional[str]] = mapped_column(String(500), comment="主图")
    images: Mapped[Optional[str]] = mapped_column(JSON, comment="组图")
    desc: Mapped[Optional[str]] = mapped_column("desc", Text, comment="详情")
    score: Mapped[int] = mapped_column(Integer, default=0, comment="消耗积分")
    weigh: Mapped[int] = mapped_column(Integer, default=0, comment="权重")
    stock: Mapped[int] = mapped_column(Integer, default=0, comment="库存")
    sales: Mapped[int] = mapped_column(Integer, default=0, comment="销售量")
    is_switch: Mapped[int] = mapped_column(Integer, default=1, comment="是否上架(0否,1是)")


class ScoreOrder(BaseMixin, Base):
    """积分兑换订单表"""
    __tablename__ = "go2run_score_order"

    uid: Mapped[int] = mapped_column(BigInteger, index=True, comment="用户id")
    order_id: Mapped[str] = mapped_column(String(50), unique=True, comment="订单号")
    product_id: Mapped[int] = mapped_column(BigInteger, comment="积分产品id")
    product_title: Mapped[Optional[str]] = mapped_column(String(255), comment="产品标题")
    product_image: Mapped[Optional[str]] = mapped_column(String(500), comment="产品图片")
    score: Mapped[int] = mapped_column(Integer, default=0, comment="消耗积分")
    number: Mapped[int] = mapped_column(Integer, default=1, comment="数量")
    total_score: Mapped[int] = mapped_column(Integer, default=0, comment="总积分")
    real_name: Mapped[Optional[str]] = mapped_column(String(100), comment="收货人姓名")
    user_phone: Mapped[Optional[str]] = mapped_column(String(20), comment="收货人电话")
    user_address: Mapped[Optional[str]] = mapped_column(String(500), comment="收货地址")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="状态(0待发货,1待收货,2已收货,3已完成)")
    delivery_name: Mapped[Optional[str]] = mapped_column(String(100), comment="快递名称")
    delivery_id: Mapped[Optional[str]] = mapped_column(String(100), comment="快递单号")
    mark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
    shop_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="门店id")
