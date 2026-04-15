from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Boolean, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BaseMixin:
    """Common fields for all entities."""
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    creator: Mapped[str | None] = mapped_column(String(64), default=None)
    updater: Mapped[str | None] = mapped_column(String(64), default=None)
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    tenant_id: Mapped[int] = mapped_column(BigInteger, default=0)
