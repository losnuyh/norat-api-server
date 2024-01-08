from typing import Annotated

from fastapi import APIRouter, Body, Query, status, Depends

from application.domain.user.use_case.port.input import UserInputPort
from application.infra.fastapi import WithFastAPIRouter
from application.infra.fastapi.auth import get_authenticated_phone

from .dto import CheckUserAccountDuplicationResponse, UserSignupRequest, UserSignupResponse

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

    def signup(self):
        @user_router.post(
            path="",
            tags=["user"],
            summary="회원 가입",
            description="</br>".join(["회원가입 합니다.", "가입 요칭시 phone 인증 토큰을 필요로 합니다."]),
            status_code=status.HTTP_200_OK,
            response_description="유저 정보",
            responses={
                status.HTTP_200_OK: {
                    "model": UserSignupResponse,
                    "description": "가입 성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "가입 실패",
                },
            },
        )
        async def handler(
            phone: Annotated[str, Depends(get_authenticated_phone)],
            body: Annotated[UserSignupRequest, Body()],
        ):
            user = await self.input.create_user_with_password(
                password=body.password,
                account=body.account,
                phone=phone,
                birth=body.birth,
            )
            assert user.id is not None
            return UserSignupResponse(
                id=user.id,
                account=user.account,
                birth=user.birth,
            )
