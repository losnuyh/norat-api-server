from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SchoolMemberTable(Base):
    __tablename__ = "school_member"

    id: Mapped[int] = mapped_column(primary_key=True, kw_only=True)
    school_code: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        kw_only=True,
        index=True,
    )
    grade: Mapped[int] = mapped_column(
        nullable=False,
        kw_only=True,
    )
    user_id: Mapped[int] = mapped_column(
        nullable=False,
        kw_only=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        kw_only=True,
    )
