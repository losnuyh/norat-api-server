from pydantic import BaseModel, Field

from application.domain.school_board.model import SchoolVO


class SchoolSearchResultResponse(BaseModel):
    results: list[SchoolVO] = Field(
        title="학교 정보",
        kw_only=True,
    )
