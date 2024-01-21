from abc import ABC, abstractmethod
from dataclasses import dataclass

from application.domain.school_board.model import PublicPost, QueueItem, School


@dataclass(kw_only=True)
class UserSchoolInfo:
    school: School
    grade: int


@dataclass
class SchoolBoardInfo:
    school: School
    grade: int
    total_member_count: int


@dataclass
class PostWriteInput:
    title: str
    content: str


class SchoolBoardInputPort(ABC):
    @abstractmethod
    async def search_school(self, *, keyword: str) -> list[School]:
        ...

    @abstractmethod
    async def register_school_member(self, *, school_code: str, user_id: int, grade: int):
        ...

    @abstractmethod
    async def get_user_school(self, *, user_id: int) -> UserSchoolInfo:
        ...

    @abstractmethod
    async def get_school_board_info(self, *, school_code: str, grade: int) -> SchoolBoardInfo:
        ...

    @abstractmethod
    async def write_post(self, *, school_code: str, grade: int, writer_id: int, title: str, content: str) -> QueueItem:
        ...

    @abstractmethod
    async def get_user_queue(self, *, school_code: str, grade: int, user_id: int) -> list[QueueItem]:
        ...

    @abstractmethod
    async def delete_user_post_in_queue(self, *, school_code: str, grade: int, user_id: int, post_item_id: int):
        ...

    @abstractmethod
    async def get_posts(
        self, *, user_id: int, school_code: str, grade: int, last_post_id: int | None = None
    ) -> list[PublicPost]:
        ...
