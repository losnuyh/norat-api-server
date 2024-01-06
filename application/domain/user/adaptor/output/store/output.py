from datetime import datetime, timezone

from sqlalchemy import select

from application.domain.user.adaptor.output.store import UserTable
from application.domain.user.model.user import User
from application.domain.user.use_case.port.output import UserStoreOutputPort


class UserStoreAdaptor(UserStoreOutputPort):
    async def get_user_by_account(self, *, account: str) -> User | None:
        stmt = select(UserTable).where(UserTable.account == account)
        user_result: UserTable = self.session.scalar(stmt)
        if user_result is None:
            return None
        return User(
            id=user_result.id,
            account=user_result.account,
            birth=user_result.birth,
        )

    async def save_user(self, *, user: User) -> User:
        now = datetime.now(tz=timezone.utc)
        user_row = UserTable(
            account=user.account,
            birth=user.birth,
            created_at=now,
        )
        self.session.add(user_row)
        user.id = user_row.id
        return user