from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import BaseMixin


class StoreTable(BaseMixin, Base):
    """桌号管理表"""
    __tablename__ = "go2run_store_table"

    shop_id: Mapped[int] = mapped_column(BigInteger, default=1, comment="门店ID")
    table_no: Mapped[str] = mapped_column(String(50), comment="桌号")
    area: Mapped[Optional[str]] = mapped_column(String(100), default=None, comment="区域(如大厅/包间)")
    seats: Mapped[int] = mapped_column(Integer, default=4, comment="座位数")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="状态(0禁用,1启用)")
    qr_url: Mapped[Optional[str]] = mapped_column(String(500), default=None, comment="二维码URL")
    last_settled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, comment="上次结算时间")
