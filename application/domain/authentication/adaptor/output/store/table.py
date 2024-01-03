from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AuthPhoneTable(Base):
    __tablename__ = "auth_phone"

    id: Mapped[int] = mapped_column(primary_key=True, kw_only=True)
    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        kw_only=True,
        index=True,
    )
    expired_at: Mapped[datetime] = mapped_column(
        nullable=False,
        kw_only=True,
    )
    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        kw_only=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        kw_only=True,
    )