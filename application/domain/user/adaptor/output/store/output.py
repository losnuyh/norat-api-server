from datetime import datetime, timezone

from sqlalchemy import select

from application.domain.user.model.user import User
from application.domain.user.use_case.port.output import UserStoreOutputPort

from .table import UserTable


class UserStoreAdaptor(UserStoreOutputPort):
    async def get_user_by_account(self, *, account: str) -> User | None:
        stmt = select(UserTable).where(UserTable.account == account)
        user_result: UserTable = await self.session.scalar(stmt)
        if user_result is None:
            return None
        return User(
            id=user_result.id,
            account=user_result.account,
            phone=user_result.phone,
            birth=user_result.birth,
        )

    async def get_user_by_user_id(self, *, user_id: int) -> User | None:
        stmt = select(UserTable).where(UserTable.id == user_id)
        user_result: UserTable = await self.session.scalar(stmt)
        if user_result is None:
            return None
        return User(
            id=user_result.id,
            account=user_result.account,
            phone=user_result.phone,
            birth=user_result.birth,
        )

    async def save_user(self, *, user: User) -> User:
        now = datetime.now(tz=timezone.utc)
        user_row = UserTable(
            account=user.account,
            phone=user.phone,
            birth=user.birth,
            created_at=now,
        )
        self.session.add(user_row)
        await self.session.flush()
        user.id = user_row.id
        return user
