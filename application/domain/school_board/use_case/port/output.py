from abc import ABC, abstractmethod
from typing import Protocol

from application.domain.school_board.model import Post, QueueItem, School, SchoolMember
from application.domain.user.model import User
from application.infra.unit_of_work.sqlalchemy import UnitOfWork


class SchoolSearchOutputPort(ABC):
    @abstractmethod
    async def search_school_by_name(self, *, keyword: str) -> list[School]:
        ...

    @abstractmethod
    async def get_school_by_code(self, *, school_code: str) -> School | None:
        ...


class SchoolStoreOutputPort(UnitOfWork, ABC):
    @abstractmethod
    async def save_school_member(self, *, member: SchoolMember):
        ...

    @abstractmethod
    async def get_user_school_member(self, *, user_id: int) -> SchoolMember | None:
        ...

    @abstractmethod
    async def get_school_member_count(self, *, school_code: str, grade: int) -> int:
        ...

    @abstractmethod
    async def save_post(self, *, post: Post):
        ...

    @abstractmethod
    async def get_user_queue_item(self, *, user_id: int, school_code: str, grade: int) -> list[QueueItem]:
        ...

    @abstractmethod
    async def save_queue_item(self, *, item: QueueItem):
        ...

    @abstractmethod
    async def delete_queue_item(self, *, item: QueueItem):
        ...


class UserOutputPort(Protocol):
    async def get_user_by_user_id(self, *, user_id: int) -> User:
        ...
