from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert

from application.domain.school_board.model import Post, QueueItem, SchoolMember
from application.domain.school_board.use_case.port.output import SchoolStoreOutputPort

from .table import QueueItemTable, SchoolMemberCountTable, SchoolMemberTable


class SchoolStoreOutputAdaptor(SchoolStoreOutputPort):
    async def save_school_member(self, *, member: SchoolMember):
        now = datetime.now(tz=timezone.utc)
        school_member_row = dict(
            id=member.id,
            school_code=member.school_code,
            grade=member.grade,
            user_id=member.user_id,
        )
        stmt = (
            insert(SchoolMemberTable)
            .values(
                created_at=now,
                **school_member_row,
            )
            .on_duplicate_key_update(
                **school_member_row,
            )
        )
        result = await self.session.execute(stmt)
        member.id, *_ = result.inserted_primary_key_rows[0]

        stmt = (
            insert(SchoolMemberCountTable)
            .values(
                school_code=member.school_code,
                grade=member.grade,
                member_count=1,
            )
            .on_duplicate_key_update(
                school_code=member.school_code,
                grade=member.grade,
                member_count=SchoolMemberCountTable.__table__.c.member_count + 1,
            )
        )
        await self.session.execute(stmt)

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

    async def get_school_member_count(self, *, school_code: str, grade: int) -> int:
        stmt = (
            select(SchoolMemberCountTable)
            .where(SchoolMemberCountTable.school_code == school_code)
            .where(SchoolMemberCountTable.grade == grade)
        )
        result: SchoolMemberCountTable = await self.session.scalar(stmt)
        if result is None:
            return 0
        return result.member_count

    async def save_post(self, *, post: Post):
        # post_row = dict(
        #     id=post.id,
        #     school_code=post.school_code,
        #     grade=post.grade,
        #     title=post.title,
        #     content=post.content,
        #     owner_id=post.owner_id,
        #     owner_random_nickname=post.owner_random_nickname,
        #     created_at=post.created_at,
        #     published_at=post.published_at,
        # )
        ...

    async def get_user_queue_item(self, *, user_id: int, school_code: str, grade: int) -> list[QueueItem]:
        stmt = (
            select(QueueItemTable)
            .where(QueueItemTable.writer_user_id == user_id)
            .where(QueueItemTable.school_code == school_code)
            .where(QueueItemTable.grade == grade)
            .order_by(QueueItemTable.id)
        )
        result: Sequence[QueueItemTable] = (await self.session.scalars(stmt)).all()
        items: list[QueueItem] = []

        for data in result:
            items.append(
                QueueItem(
                    id=data.id,
                    post=Post(
                        school_code=data.school_code,
                        grade=data.grade,
                        title=data.title,
                        content=data.content,
                        writer_id=data.writer_user_id,
                        writer_random_nickname=data.writer_random_nickname,
                        created_at=data.created_at,
                    ),
                    rejected_at=data.rejected_at,
                ),
            )
        return items

    async def save_queue_item(self, *, item: QueueItem):
        item_row = dict(
            id=item.id,
            rejected_at=item.rejected_at,
            school_code=item.post.school_code,
            grade=item.post.grade,
            title=item.post.title,
            content=item.post.content,
            writer_user_id=item.post.writer_id,
            writer_random_nickname=item.post.writer_random_nickname,
            created_at=item.post.created_at,
        )
        stmt = insert(QueueItemTable).values(**item_row).on_duplicate_key_update(**item_row)
        result = await self.session.execute(stmt)
        item.id, *_ = result.inserted_primary_key_rows[0]
