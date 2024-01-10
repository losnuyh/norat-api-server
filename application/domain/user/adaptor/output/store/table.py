from datetime import date, datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserTable(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, kw_only=True)
    account: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        kw_only=True,
        index=True,
        unique=True,
    )
    birth: Mapped[date] = mapped_column(nullable=False, kw_only=True)
    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        kw_only=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        kw_only=True,
    )


class CertificationTable(Base):
    __tablename__ = "certification"

    id: Mapped[int] = mapped_column(primary_key=True, kw_only=True)
    user_id: Mapped[int] = mapped_column(
        nullable=False,
        kw_only=True,
        index=True,
    )
    certification_type: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        kw_only=True,
    )
    gender: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        kw_only=True,
    )
    birth: Mapped[date] = mapped_column(nullable=False, kw_only=True)
    unique_key: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        kw_only=True,
        index=True,
    )
    unique_in_site: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        kw_only=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        kw_only=True,
    )
