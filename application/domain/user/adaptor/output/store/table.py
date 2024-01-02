from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AdminTable(Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(primary_key=True, kw_only=True)
    account: Mapped[str] = mapped_column(String(30), nullable=False, kw_only=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, kw_only=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        kw_only=True,
    )
