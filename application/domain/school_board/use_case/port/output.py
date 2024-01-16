from abc import ABC, abstractmethod
from typing import Protocol

from application.domain.school_board.model import School, SchoolMember
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


class UserOutputPort(Protocol):
    async def get_user_by_user_id(self, *, user_id: int) -> User:
        ...
