import re
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query, status

from application.domain.authentication.use_case.port.input import AuthenticationInputPort
from application.infra.fastapi import WithFastAPIRouter

from .dto import SendVerificationCodeToPhoneResponse, VerifyPhoneRequest, VerifyPhoneResponse

authentication_router = APIRouter()


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