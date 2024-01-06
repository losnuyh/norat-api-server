from typing import Annotated

from fastapi import APIRouter, Query, status

from application.domain.user.use_case.port.input import UserInputPort
from application.infra.fastapi import WithFastAPIRouter

from .dto import CheckUserAccountDuplicationResponse

user_router = APIRouter()


class UserHttpInputAdaptor(WithFastAPIRouter):
    def __init__(self, *, input: UserInputPort):
        self.input = input

    def check_account_duplication(self):
        @user_router.get(
            path="/check",
            tags=["user"],
            summary="아이디 중복 체크",
            status_code=status.HTTP_200_OK,
            response_description="아이디 중복 여부를 확인합니다.",
            responses={
                status.HTTP_200_OK: {"model": CheckUserAccountDuplicationResponse, "description": "유저 아이디 중복 체크 결과"},
            },
        )
        async def handler(account: Annotated[str, Query()]):
            is_exist = await self.input.check_account(account=account)
            return CheckUserAccountDuplicationResponse(
                account=account,
                is_exist=is_exist,
            )
