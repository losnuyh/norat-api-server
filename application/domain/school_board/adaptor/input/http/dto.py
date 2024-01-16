from pydantic import BaseModel, Field

from application.domain.school_board.model import School


class SchoolSearchResultResponse(BaseModel):
    results: list[School] = Field(
        title="학교 정보",
        kw_only=True,
    )


class RegisterSchoolMemberRequest(BaseModel):
    grade: int = Field(title="학년")
