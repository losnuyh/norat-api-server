from typing import Annotated

from fastapi import APIRouter, Query, status

from application.domain.school_board.use_case.port.input import SchoolBoardInputPort
from application.infra.fastapi import WithFastAPIRouter

from .dto import SchoolSearchResultResponse

school_board_router = APIRouter()


class SchoolBoardHttpInputAdaptor(WithFastAPIRouter):
    def __init__(self, *, input_adaptor: SchoolBoardInputPort):
        self.input = input_adaptor

    def search_school(self):
        @school_board_router.get(
            path="/search",
            tags=["school"],
            summary="학교 이름 검색",
            description="</br>".join(
                [
                    "학교 이름을 검색합니다.",
                    "검색 키워드는 최소 2글자, 최대 10글자입니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            response_description="학교 검색 결과",
            responses={
                status.HTTP_200_OK: {
                    "model": SchoolSearchResultResponse,
                    "description": "발송 성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
            },
        )
        async def handler(keyword: Annotated[str, Query(min_length=2, max_length=10)]):
            result = await self.input.search_school(keyword=keyword)
            return SchoolSearchResultResponse(results=result)