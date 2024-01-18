from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .post import Post


@dataclass
class QueueItem:
    post: Post
    id: int | None = None
    rejected_at: datetime | None = None
