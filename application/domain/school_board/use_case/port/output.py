from abc import ABC, abstractmethod

from application.domain.school_board.model import SchoolVO


class SchoolSearchOutputPort(ABC):
    @abstractmethod
    async def search_school_by_name(self, *, keyword: str) -> list[SchoolVO]:
        ...

    # @abstractmethod
    # async def search_school_by_id(self, *, school_id: str) -> SchoolVO | None:
    #     ...
    #
