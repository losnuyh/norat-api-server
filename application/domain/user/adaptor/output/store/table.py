from datetime import datetime, date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserTable(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, kw_only=True)
    account: Mapped[str] = mapped_column(
        String(30), nullable=False, kw_only=True, index=True, unique=True,
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
