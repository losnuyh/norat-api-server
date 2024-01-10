from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from application.domain.user.model import User
from application.domain.user.use_case.port.input import UserInputPort
from application.error import PermissionDenied
from application.infra.fastapi import WithFastAPIRouter
from application.infra.fastapi.auth import (
    get_authenticated_phone,
    get_authenticated_phone_or_user,
    get_authenticated_user,
)

from .dto import (
    CertificationRequest,
    CheckUserAccountDuplicationResponse,
    UserResponse,
    UserSignupRequest,
    UserSignupResponse,
)

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

    def certificate_self(self):
        @user_router.post(
            path="/{user_id}/certification/self",
            tags=["user"],
            summary="본인 인증 완료 요청",
            description="</br>".join(
                [
                    "포트원 본인인증 완료 후, 인증 완료 처리를 서버에 요청합니다.",
                    "포트원 본인인증 후 받은 imp_uid를 전송합니다.",
                    "본인 인증인 경우에만 가능합니다. 부모 인증은 허용하지 않습니다.",
                    "가입시 입력한 정보가 14세 미만인 경우에는 본인인증 api를 호출할 수 없습니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "실패",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            body: Annotated[CertificationRequest, Body()],
            request_user_id: Annotated[str, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            await self.input.certificate_self(user_id=user_id, imp_uid=body.imp_uid)
            return {"message": "success"}

    def certificate_guardian(self):
        @user_router.post(
            path="/{user_id}/certification/guardian",
            tags=["user"],
            summary="보호자 인증 완료 요청",
            description="</br>".join(
                [
                    "포트원 보호자 완료 후, 인증 완료 처리를 서버에 요청합니다.",
                    "포트원 보호자 후 받은 imp_uid를 전송합니다.",
                    "보호자 인증인 경우에만 가능합니다.",
                    "가입시 입력한 정보가 14세 이상인 경우에는 보호자인증 api를 호출할 수 없습니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "실패",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            body: Annotated[CertificationRequest, Body()],
            request_user_id: Annotated[str, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            await self.input.certificate_guardian(user_id=user_id, imp_uid=body.imp_uid)
            return {"message": "success"}

    def get_my_info(self):
        @user_router.post(
            path="/me",
            tags=["user"],
            summary="내 정보 가져오기",
            description="</br>".join(
                [
                    "????",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "실패",
                },
            },
        )
        async def handler(
            authenticated: Annotated[tuple, Depends(get_authenticated_phone_or_user)],
        ):
            authenticated_entity, value = authenticated
            user: User | None = None
            match authenticated_entity:
                case "phone":
                    user = await self.input.get_user_by_phone(phone=value)
                case "user_id":
                    user = await self.input.get_user_by_user_id(user_id=value)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="user not found",
                )
            assert user.id is not None
            return UserResponse(
                id=user.id,
                account=user.account,
                birth=user.birth,
            )
