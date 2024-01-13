from datetime import date, datetime

from pydantic import BaseModel, Field


class CheckUserAccountDuplicationResponse(BaseModel):
    account: str = Field(
        title="중복 체크 요청한 account",
        min_length=2,
        max_length=12,
    )
    is_exist: bool = Field(
        title="중복 여부",
    )


class UserSignupRequest(BaseModel):
    account: str = Field(
        title="유저 계정",
        min_length=2,
        max_length=12,
    )
    birth: date = Field(title="생일 정보")
    password: str = Field(
        title="비밀번호",
        min_length=8,
        max_length=32,
    )


class UserSignupResponse(BaseModel):
    id: int = Field(title="유저 아이디")
    account: str = Field(title="유저 계정")
    birth: date = Field(title="생일 정보")


class CertificationRequest(BaseModel):
    imp_uid: str = Field(title="포트원 imp uid")


class UserResponse(BaseModel):
    id: int
    account: str
    birth: date
    verified_at: datetime | None = None
    school_name: str | None = None
    school_grade: int | None = None

    privacy_policy_agreed_at: datetime | None = None
    terms_policy_agreed_at: datetime | None = None
    marketing_policy_agreed_at: datetime | None = None
    push_agreed_at: datetime | None = None


class AgreeTermsRequest(BaseModel):
    marketing: bool = Field(title="마케팅 동의")
    push: bool = Field(title="푸시 동의")


class PreSignedUrlResponse(BaseModel):
    pre_signed_url: str = Field(title="pre signed url")
    key: str = Field(title="s3 키")


class RequestFaceVerificationRequest(BaseModel):
    key: str = Field(title="s3 키")


class GetLastFaceVerificationRequestResponse(BaseModel):
    requested_at: datetime
    changed_at: datetime
    status: str
