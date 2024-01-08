import re
from functools import partial
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from application.domain.authentication.use_case.port.input import AuthenticationInputPort
from application.infra.fastapi import WithFastAPIRouter
from application.infra.fastapi.auth import get_authenticated_user

from .dto import (
    ChangePasswordRequest,
    SendVerificationCodeToPhoneResponse,
    UserLoginRequest,
    UserTokenRefreshRequest,
    UserTokenResponse,
    VerifyPhoneRequest,
    VerifyPhoneResponse,
)

authentication_router = APIRouter()


get_authenticated_user_for_refresh = partial(get_authenticated_user, verify_exp=False)


def is_valid_phone(string):
    pattern = r"^010\d{8}$"
    if re.match(pattern, string):
        return True
    else:
        return False


class AuthenticationHttpInputAdaptor(WithFastAPIRouter):
    def __init__(
        self,
        *,
        input_adaptor: AuthenticationInputPort,
    ):
        self.input = input_adaptor

    def send_verification_code_phone(self):
        @authentication_router.get(
            path="/phone",
            tags=["auth"],
            summary="인증코드 발송",
            description="""핸드폰번호로 인증 코드를 발송합니다.</br>
            다시 요청하는 경우, 이전 인증코드는 유효하지 않습니다.</br>""",
            status_code=status.HTTP_202_ACCEPTED,
            response_description="인증코드가 발송된 연락처",
            responses={
                status.HTTP_202_ACCEPTED: {
                    "model": SendVerificationCodeToPhoneResponse,
                    "description": "발송 성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
            },
        )
        async def handler(phone: Annotated[str, Query(min_length=11, max_length=11)]):
            if not is_valid_phone(phone):
                raise HTTPException(
                    status_code=400,
                    detail="잘못된 핸드폰 번호 형식입니다. ex) 010XXXXXXXX",
                )
            await self.input.send_verification_code_to_phone(phone_number=phone)
            return SendVerificationCodeToPhoneResponse(to=phone)

    def verify_phone(self):
        @authentication_router.post(
            path="/phone",
            tags=["auth"],
            summary="발송된 인증코드로 연락처 인증",
            description="""핸드폰 번호로 발송된 인증코드로 핸드폰 번호를 인증합니다.</br>
            올바른 인증코드인 경우 인증된 핸드폰 번호를 증명할 수 있는 토큰이 발행됩니다.</br>
            해당 토큰과 핸드폰 번호를 해더에 담아서 회원가입을 진행할 수 있습니다.</br>""",
            status_code=status.HTTP_200_OK,
            response_description="인증된 핸드폰 번호를 증명하는 토큰",
            responses={
                status.HTTP_200_OK: {
                    "model": VerifyPhoneResponse,
                    "description": "인증 성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "인증 실패",
                },
            },
        )
        async def handler(
            body: Annotated[VerifyPhoneRequest, Body()],
        ):
            if not is_valid_phone(body.phone):
                raise HTTPException(
                    status_code=400,
                    detail="잘못된 핸드폰 번호 형식입니다. ex) 010XXXXXXXX",
                )
            phone_token = await self.input.get_phone_verification_token(
                phone=body.phone,
                code=body.code,
            )
            return VerifyPhoneResponse(verified_phone_token=phone_token.access_token)

    def login_with_password(self):
        @authentication_router.post(
            path="/login",
            tags=["auth"],
            summary="로그인",
            description="</br>".join(["비밀번호로 로그인하여 토큰을 획득합니다."]),
            status_code=status.HTTP_200_OK,
            response_description="토큰과 리프레쉬 토큰",
            responses={
                status.HTTP_200_OK: {
                    "model": UserTokenResponse,
                    "description": "로그인 성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "로그인 실패",
                },
            },
        )
        async def handler(
            body: Annotated[UserLoginRequest, Body()],
        ):
            token = await self.input.login_user_with_password(account=body.account, password=body.password)
            return UserTokenResponse(
                access_token=token.access_token,
                refresh_token=token.refresh_token,
            )

    def refresh_token(self):
        @authentication_router.post(
            path="/refresh",
            tags=["auth"],
            summary="토큰 재발급",
            description="</br>".join(
                ["리프레쉬 토큰으로 토큰을 재발급합니다.", "리프레쉬토큰은 로그인때 발급받은 데이터를 사용합니다.", "리프레쉬 토큰 유효 기간은 1년입니다."],
            ),
            status_code=status.HTTP_200_OK,
            response_description="토큰과 리프레쉬 토큰",
            responses={
                status.HTTP_200_OK: {
                    "model": UserTokenResponse,
                    "description": "재발급 성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "재발급 실패",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Depends(get_authenticated_user_for_refresh)],
            body: Annotated[UserTokenRefreshRequest, Body()],
        ):
            token = await self.input.refresh_user_token(
                user_id=user_id,
                refresh_token=body.refresh_token,
            )
            return UserTokenResponse(
                access_token=token.access_token,
                refresh_token=token.refresh_token,
            )

    def change_password(self):
        @authentication_router.put(
            path="/password",
            tags=["auth"],
            summary="비밀번호 변경",
            description="</br>".join(
                ["비밀번호를 변경합니다.", "이번 비밀번호와 새로 사용할 비밀번호를 요청에 포함해야합니다."],
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
            user_id: Annotated[int, Depends(get_authenticated_user_for_refresh)],
            body: Annotated[ChangePasswordRequest, Body()],
        ):
            await self.input.change_password(
                user_id=user_id,
                password=body.password,
                new_password=body.new_password,
            )
            return {"message": "success"}
