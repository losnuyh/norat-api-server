from abc import ABC, abstractmethod

from application.domain.school_board.model import SchoolVO


class SchoolBoardInputPort(ABC):
    @abstractmethod
    async def search_school(self, *, keyword: str) -> list[SchoolVO]:
        ...
