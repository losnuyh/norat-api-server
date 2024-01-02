from pydantic import BaseModel, Field


class SendVerificationCodeToPhoneResponse(BaseModel):
    to: str = Field(
        title="핸드폰 번호",
        description="인증코드를 발송한 핸드폰 번호",
    )


class VerifyPhoneRequest(BaseModel):
    phone: str = Field(
        title="인증할 핸드폰 번호",
        description="인증 코드를 발송 받은 핸드폰 번호를 입력합니다.",
        min_length=11,
        max_length=11,
    )
    code: str = Field(
        title="인증 코드",
        description="핸드폰으로 발송된 인증코드를 입력합니다.",
    )


class VerifyPhoneResponse(BaseModel):
    verified_phone_token: str = Field(
        title="인증 증명 토큰",
        description="핸드폰 번호 인증을 증명하는 토큰",
    )
