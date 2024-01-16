from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert

from application.domain.school_board.model import SchoolMember
from application.domain.school_board.use_case.port.output import SchoolStoreOutputPort

from .table import SchoolMemberTable


class SchoolStoreOutputAdaptor(SchoolStoreOutputPort):
    async def save_school_member(self, *, member: SchoolMember):
        now = datetime.now(tz=timezone.utc)
        school_student_row = dict(
            id=member.id,
            school_code=member.school_code,
            grade=member.grade,
            user_id=member.user_id,
        )
        stmt = (
            insert(SchoolMemberTable)
            .values(
                created_at=now,
                **school_student_row,
            )
            .on_duplicate_key_update(
                **school_student_row,
            )
        )
        result = await self.session.execute(stmt)
        member.id, *_ = result.inserted_primary_key_rows[0]

    async def get_user_school_member(self, *, user_id: int) -> SchoolMember | None:
        stmt = select(SchoolMemberTable).where(SchoolMemberTable.user_id == user_id)
        result: SchoolMemberTable = await self.session.scalar(stmt)
        if result is None:
            return None
        return SchoolMember(
            id=result.id,
            user_id=result.user_id,
            grade=result.grade,
            school_code=result.school_code,
        )
