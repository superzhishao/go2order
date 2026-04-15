from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Integer, BigInteger, DECIMAL, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import BaseMixin


class Coupon(BaseMixin, Base):
    """优惠券表"""
    __tablename__ = "go2run_coupon"

    shop_id: Mapped[Optional[str]] = mapped_column(String(255), default="0", comment="店铺id(0通用)")
    shop_name: Mapped[Optional[str]] = mapped_column(String(500), comment="店铺名称")
    title: Mapped[str] = mapped_column(String(255), comment="优惠券名称")
    is_switch: Mapped[int] = mapped_column(Integer, default=1, comment="是否上架")
    least: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="消费多少可用")
    value: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="优惠券金额")
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="开始时间")
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="结束时间")
    weigh: Mapped[int] = mapped_column(Integer, default=0, comment="权重")
    type: Mapped[int] = mapped_column(Integer, default=0, comment="可用类型(0通用,1自取,2外卖)")
    exchange_code: Mapped[Optional[str]] = mapped_column(String(100), comment="兑换码")
    receive: Mapped[int] = mapped_column(Integer, default=0, comment="已领取")
    distribute: Mapped[int] = mapped_column(Integer, default=0, comment="发行数量")
    score: Mapped[int] = mapped_column(Integer, default=0, comment="所需积分")
    instructions: Mapped[Optional[str]] = mapped_column(Text, comment="使用说明")
    image: Mapped[Optional[str]] = mapped_column(String(500), comment="图片")
    limit: Mapped[int] = mapped_column("limit", Integer, default=1, comment="限领数量")


class CouponUser(BaseMixin, Base):
    """用户优惠券表"""
    __tablename__ = "go2run_coupon_user"

    uid: Mapped[int] = mapped_column(BigInteger, index=True, comment="用户id")
    coupon_id: Mapped[int] = mapped_column(BigInteger, index=True, comment="优惠券id")
    coupon_title: Mapped[Optional[str]] = mapped_column(String(255), comment="优惠券名称")
    coupon_value: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="优惠券金额")
    coupon_least: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="最低消费")
    use_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="使用时间")
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="有效开始时间")
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="有效结束时间")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="状态(0未使用,1已使用,2已过期)")
    shop_id: Mapped[Optional[str]] = mapped_column(String(255), comment="店铺id")
    type: Mapped[int] = mapped_column(Integer, default=0, comment="可用类型(0通用,1自取,2外卖)")
