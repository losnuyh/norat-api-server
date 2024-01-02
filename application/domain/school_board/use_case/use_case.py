from application.domain.school_board.model import SchoolVO
from application.domain.school_board.use_case.port.input import SchoolBoardInputPort
from application.domain.school_board.use_case.port.output import SchoolSearchOutputPort


class SchoolBoardUseCase(SchoolBoardInputPort):
    def __init__(self, *, search_output: SchoolSearchOutputPort):
        self.school_search_output = search_output

    async def search_school(self, *, keyword: str) -> list[SchoolVO]:
        search_list = await self.school_search_output.search_school_by_name(keyword=keyword)
        if not search_list:
            return []
        return search_list[:5]
