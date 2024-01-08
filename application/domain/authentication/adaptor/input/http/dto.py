from datetime import date

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


class UserSignupRequest(BaseModel):
    account: str = Field(title="유저 계정")
    birth: date = Field(title="생일 정보")
    password: str = Field(title="비밀번호")


class UserSignupResponse(BaseModel):
    id: int = Field(title="유저 아이디")
    account: str = Field(title="유저 계정")
    birth: date = Field(title="생일 정보")


class UserLoginRequest(BaseModel):
    account: str = Field(title="유저 아이디")
    password: str = Field(title="유저 비밀번호")


class UserTokenResponse(BaseModel):
    access_token: str = Field(title="엑세스 토큰")
    refresh_token: str = Field(title="리프레쉬 토큰")
