from pydantic import BaseModel, Field


class CheckUserAccountDuplicationResponse(BaseModel):
    account: str = Field(title="중복 체크 요청한 account")
    is_exist: bool = Field(
        title="중복 여부",
    )
