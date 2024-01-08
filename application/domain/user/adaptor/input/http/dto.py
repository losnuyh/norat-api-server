from datetime import date

from pydantic import BaseModel, Field


class CheckUserAccountDuplicationResponse(BaseModel):
    account: str = Field(title="중복 체크 요청한 account")
    is_exist: bool = Field(
        title="중복 여부",
    )


class UserSignupRequest(BaseModel):
    account: str = Field(title="유저 계정")
    birth: date = Field(title="생일 정보")
    password: str = Field(title="비밀번호")


class UserSignupResponse(BaseModel):
    id: int = Field(title="유저 아이디")
    account: str = Field(title="유저 계정")
    birth: date = Field(title="생일 정보")
