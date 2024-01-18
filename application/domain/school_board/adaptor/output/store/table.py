from datetime import datetime

from sqlalchemy import Index, String, UniqueConstraint
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


class SchoolMemberCountTable(Base):
    __tablename__ = "school_member_count"

    id: Mapped[int] = mapped_column(primary_key=True, kw_only=True)
    school_code: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        kw_only=True,
    )
    grade: Mapped[int] = mapped_column(
        nullable=False,
        kw_only=True,
    )
    member_count: Mapped[int] = mapped_column(
        default=0,
    )
    __table_args__ = (UniqueConstraint("school_code", "grade", name="school_grade_uc"),)


class PostData:
    school_code: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        kw_only=True,
    )
    grade: Mapped[int] = mapped_column(
        nullable=False,
        kw_only=True,
    )
    title: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        kw_only=True,
    )
    content: Mapped[str] = mapped_column(
        String(280),
        nullable=True,
        kw_only=True,
    )
    writer_user_id: Mapped[int] = mapped_column(
        nullable=False,
        kw_only=True,
        index=True,
    )
    writer_random_nickname: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        kw_only=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        kw_only=True,
    )


class QueueItemTable(PostData, Base):
    __tablename__ = "queue_item"

    id: Mapped[int] = mapped_column(primary_key=True, kw_only=True)
    rejected_at: Mapped[datetime] = mapped_column(
        nullable=True,
        kw_only=True,
    )
    __table_args__ = (Index("queue_item_per_user_idx", "writer_user_id", "school_code", "grade"),)
