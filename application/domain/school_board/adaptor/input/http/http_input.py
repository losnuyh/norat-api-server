from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status

from application.domain.school_board.use_case.port.input import SchoolBoardInputPort
from application.error import PermissionDenied
from application.infra.fastapi import WithFastAPIRouter
from application.infra.fastapi.auth import get_authenticated_user

from .dto import RegisterSchoolMemberRequest, SchoolSearchResultResponse, UserSchoolInfoResponse

school_board_router = APIRouter()
user_router_in_school_board = APIRouter()


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

    def register_school_member(self):
        @school_board_router.post(
            path="/{school_code}/member",
            tags=["school"],
            summary="학교 등록 합니다.",
            description="</br>".join(
                [
                    "학교 등록",
                ],
            ),
            status_code=status.HTTP_200_OK,
            response_description="학교 맴버로 등록",
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
        async def handler(
            school_code: Annotated[str, Path()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
            body: Annotated[RegisterSchoolMemberRequest, Body()],
        ):
            await self.input.register_school_member(
                school_code=school_code,
                user_id=request_user_id,
                grade=body.grade,
            )
            return {"message": "success"}

    def get_user_school_info(self):
        @user_router_in_school_board.get(
            path="/{user_id}/school",
            tags=["school", "user"],
            summary="유저 학교 정보 획득",
            description="</br>".join(
                [
                    "유저의 학교 정보를 획득합니다.",
                    "학교를 이미 등록한 경우에만 확인할 수 있습니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            response_description="학교 맴버로 등록",
            responses={
                status.HTTP_200_OK: {
                    "model": UserSchoolInfoResponse,
                    "description": "발송 성공",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")
            info = await self.input.get_user_school(
                user_id=request_user_id,
            )
            return UserSchoolInfoResponse(
                info=info,
            )
