from abc import ABC, abstractmethod
from dataclasses import dataclass

from application.domain.school_board.model import School


@dataclass(kw_only=True)
class UserSchoolInfo:
    school: School
    grade: int


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
