from datetime import datetime

from pydantic import BaseModel, Field

from application.domain.school_board.model import School
from application.domain.school_board.use_case.port.input import SchoolBoardInfo, UserSchoolInfo


class SchoolSearchResultResponse(BaseModel):
    results: list[School] = Field(
        title="학교 정보",
        kw_only=True,
    )


class RegisterSchoolMemberRequest(BaseModel):
    grade: int = Field(title="학년")


class UserSchoolInfoResponse(BaseModel):
    info: UserSchoolInfo = Field(title="유저가 등록한 학교 정보")


class SchoolBoardInfoResponse(BaseModel):
    info: SchoolBoardInfo = Field(title="학교 학년 게시판 상태")


class WritePostRequest(BaseModel):
    title: str
    content: str


class QueueItemResponse(BaseModel):
    id: int
    title: str
    content: str
    random_nickname: str
    created_at: datetime
    rejected_at: datetime | None
