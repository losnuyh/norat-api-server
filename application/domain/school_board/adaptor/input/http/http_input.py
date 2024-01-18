from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status

from application.domain.school_board.use_case.port.input import SchoolBoardInputPort
from application.error import PermissionDenied
from application.infra.fastapi import WithFastAPIRouter
from application.infra.fastapi.auth import get_authenticated_user

from .dto import (
    QueueItemResponse,
    RegisterSchoolMemberRequest,
    SchoolBoardInfoResponse,
    SchoolSearchResultResponse,
    UserSchoolInfoResponse,
    WritePostRequest,
)

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

    def get_school_board_info(self):
        @school_board_router.get(
            path="/{school_code}/grade/{grade}",
            tags=["school"],
            summary="학교 상태 확인",
            description="</br>".join(
                [
                    "학교 + 학년 등록 상태를 확인 확인합니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            response_description="학교+학년 정보 확인",
            responses={
                status.HTTP_200_OK: {
                    "model": SchoolBoardInfoResponse,
                    "description": "학교 학년 게시판 상태 정보",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
            },
        )
        async def handler(
            school_code: Annotated[str, Path()],
            grade: Annotated[int, Path()],
            _: Annotated[int, Depends(get_authenticated_user)],
        ):
            info = await self.input.get_school_board_info(
                school_code=school_code,
                grade=grade,
            )
            return SchoolBoardInfoResponse(
                info=info,
            )

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

    def write_post(self):
        @school_board_router.post(
            path="/{school_code}/grade/{grade}/post/queue",
            tags=["queue"],
            summary="학교 게시판에 대기 큐에 글 작성하기",
            description="</br>".join(
                [
                    "등록한 학교 학년 게시판 대기 큐에 글을 작성합니다.",
                    "내 큐에 글이 5개 이상이면 더이상 작성할 수 없습니다",
                    "- 타이밍 이슈로 5개가 넘을 수 있습니다.",
                    "작성한 글은 대기 큐에서 심사를 기다립니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            response_description="대기 큐에 글 작성 결과",
            responses={
                status.HTTP_200_OK: {
                    "model": QueueItemResponse,
                    "description": "발송 성공",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
            school_code: Annotated[str, Path()],
            grade: Annotated[int, Path()],
            body: Annotated[WritePostRequest, Body()],
        ):
            item = await self.input.write_post(
                school_code=school_code,
                grade=grade,
                writer_id=request_user_id,
                title=body.title,
                content=body.content,
            )
            assert item.id is not None
            return QueueItemResponse(
                id=item.id,
                title=item.post.title,
                content=item.post.content,
                random_nickname=item.post.writer_random_nickname,
                created_at=item.post.created_at,
                rejected_at=item.rejected_at,
            )

    def get_my_post_in_queue(self):
        @school_board_router.get(
            path="/{school_code}/grade/{grade}/post/queue",
            tags=["queue"],
            summary="내 대기 큐에 있는 포스트 보기",
            description="</br>".join(
                [
                    "대기중인 글을 확인할 수 있습니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            response_description="대기 큐 글 목록",
            responses={
                status.HTTP_200_OK: {
                    "model": list[QueueItemResponse],
                    "description": "발송 성공",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
            school_code: Annotated[str, Path()],
            grade: Annotated[int, Path()],
        ):
            result = await self.input.get_user_queue(
                school_code=school_code,
                grade=grade,
                user_id=request_user_id,
            )
            return [
                QueueItemResponse(
                    id=item.id,
                    title=item.post.title,
                    content=item.post.content,
                    random_nickname=item.post.writer_random_nickname,
                    created_at=item.post.created_at,
                    rejected_at=item.rejected_at,
                )
                for item in result
                if item.id is not None
            ]

    def delete_my_post_in_queue(self):
        @school_board_router.delete(
            path="/{school_code}/grade/{grade}/post/queue/{post_item_id}",
            tags=["queue"],
            summary="큐에 작성한 글 지우기",
            description="</br>".join(
                [
                    "큐에 등록된 글을 제거합니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "제거 성공",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
            school_code: Annotated[str, Path()],
            grade: Annotated[int, Path()],
            post_item_id: Annotated[int, Path()],
        ):
            await self.input.delete_user_post_in_queue(
                school_code=school_code,
                grade=grade,
                user_id=request_user_id,
                post_item_id=post_item_id,
            )
            return {"message": "success"}
