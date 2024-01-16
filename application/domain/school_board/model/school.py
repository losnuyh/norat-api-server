from dataclasses import dataclass

from application.domain.user.model import User


@dataclass(kw_only=True)
class School:
    school_code: str  # SD_SCHUL_CODE
    name: str  # SCHUL_NM
    address: str  # ORG_RDNMA

    def register_member(self, user: User, grade: int):
        assert user.id is not None
        return SchoolMember(
            school_code=self.school_code,
            grade=grade,
            user_id=user.id,
        )


@dataclass(kw_only=True)
class SchoolMember:
    school_code: str
    grade: int
    user_id: int
    id: int | None = None
