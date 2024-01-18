from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass
class _PostBase:
    school_code: str
    grade: int
    title: str
    content: str
    writer_id: int
    writer_random_nickname: str
    created_at: datetime


@dataclass
class Post(_PostBase):
    id: int | None = None

    def for_public(self) -> PostForPublic:
        return PostForPublic(published_at=datetime.now(tz=timezone.utc), **asdict(self))


@dataclass
class PostForPublic(_PostBase):
    published_at: datetime
    id: int | None = None
