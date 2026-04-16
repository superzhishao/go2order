from datetime import time
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Integer, BigInteger, DECIMAL, Text, Time, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import BaseMixin


class StoreShop(BaseMixin, Base):
    """门店管理表"""
    __tablename__ = "go2run_store_shop"

    name: Mapped[str] = mapped_column(String(255), comment="店铺名称")
    mobile: Mapped[Optional[str]] = mapped_column(String(20), comment="店铺电话")
    image: Mapped[Optional[str]] = mapped_column(String(500), comment="图片")
    images: Mapped[Optional[str]] = mapped_column(JSON, comment="多张图片")
    address: Mapped[Optional[str]] = mapped_column(String(500), comment="详细地址")
    address_map: Mapped[Optional[str]] = mapped_column(String(500), comment="地图定位地址")
    lng: Mapped[Optional[str]] = mapped_column(String(50), comment="经度")
    lat: Mapped[Optional[str]] = mapped_column(String(50), comment="纬度")
    distance: Mapped[int] = mapped_column(Integer, default=0, comment="外卖配送距离(千米),0不送外卖")
    min_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="起送价钱")
    delivery_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="配送价格")
    notice: Mapped[Optional[str]] = mapped_column(Text, comment="公告")
    notice_i18n: Mapped[Optional[dict]] = mapped_column(JSON, comment="公告多语言")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="是否营业(0否,1是)")
    admin_id: Mapped[Optional[str]] = mapped_column(JSON, comment="管理员id")
    uniprint_id: Mapped[Optional[str]] = mapped_column(String(255), comment="打印机id")
    start_time: Mapped[Optional[str]] = mapped_column(String(20), comment="营业开始时间")
    end_time: Mapped[Optional[str]] = mapped_column(String(20), comment="营业结束时间")
    logo: Mapped[Optional[str]] = mapped_column(String(500), default=None, comment="餐厅Logo")
    theme_color: Mapped[Optional[str]] = mapped_column(String(50), default=None, comment="主题色(如#1A1A1A)")
    currency: Mapped[Optional[str]] = mapped_column(String(10), default="¥", comment="货币符号")
    enabled_languages: Mapped[Optional[str]] = mapped_column(JSON, default=None, comment="启用的客户端语言,如['en','zh']")
    default_language: Mapped[Optional[str]] = mapped_column(String(10), default=None, comment="默认客户端语言")
    domain: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment="店铺域名(用于二维码生成,如 https://example.com)")
