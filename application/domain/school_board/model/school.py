from dataclasses import dataclass, field
from datetime import datetime, timezone
from random import choice
from typing import Protocol

from application.domain.user.model import User
from application.error import ServerError

from .post import Post
from .queue import QueueItem


@dataclass(kw_only=True)
class School:
    school_code: str  # SD_SCHUL_CODE
    name: str  # SCHUL_NM
    address: str  # ORG_RDNMA

    def register_member(self, user: User, grade: int):
        assert user.id is not None
        return SchoolMember(
            school_code=self.school_code,
            grade=grade,
            user_id=user.id,
        )


def generate_random_nickname() -> str:
    adjective_list = [
        "귀여운",
        "깜찍한",
        "힘쎈",
    ]
    noun_list = [
        "토끼",
        "하마",
        "초콜릿",
    ]
    return f"{choice(adjective_list)} {choice(noun_list)}"


class QueueItemLoader(Protocol):
    async def get_user_queue_item(self, *, user_id: int, school_code: str, grade: int) -> list[QueueItem]:
        ...


@dataclass(kw_only=True)
class SchoolMember:
    school_code: str
    grade: int
    user_id: int
    id: int | None = None
    post_queue: list[QueueItem] = field(default_factory=list)
    _queue_loader: QueueItemLoader | None = None

    def write_post_and_queueing(self, title: str, content: str) -> QueueItem:
        now = datetime.now(tz=timezone.utc)
        item = QueueItem(
            post=Post(
                title=title,
                content=content,
                writer_random_nickname=generate_random_nickname(),
                created_at=now,
                school_code=self.school_code,
                grade=self.grade,
                writer_id=self.user_id,
            ),
        )
        self.post_queue.append(item)
        return item

    def set_queue_loader(self, *, loader: QueueItemLoader):
        self._queue_loader = loader

    async def load_queue_items(self):
        if self._queue_loader is None:
            raise ServerError("queue loader를 지정하지 않는 코드가 실행중입니다. 서버 개발자에게 연락이 필요합니다.")
        items = await self._queue_loader.get_user_queue_item(
            user_id=self.user_id,
            school_code=self.school_code,
            grade=self.grade,
        )
        self.post_queue = items
