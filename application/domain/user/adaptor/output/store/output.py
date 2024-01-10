from datetime import datetime, timezone

from sqlalchemy import Select, select
from sqlalchemy.dialects.mysql import insert

from application.domain.user.model import CertificationInfo, CertificationType, User
from application.domain.user.use_case.port.output import UserStoreOutputPort

from .table import CertificationTable, UserTable


class UserStoreAdaptor(UserStoreOutputPort):
    async def _get_user_table(self, select_stmt: Select) -> User | None:
        user_result: UserTable = await self.session.scalar(select_stmt)
        if user_result is None:
            return None
        return User(
            id=user_result.id,
            account=user_result.account,
            phone=user_result.phone,
            birth=user_result.birth,
            verified_at=user_result.verified_at,
        )

    async def get_user_by_account(self, *, account: str) -> User | None:
        stmt = select(UserTable).where(UserTable.account == account)
        return await self._get_user_table(stmt)

    async def get_user_by_user_id(self, *, user_id: int) -> User | None:
        stmt = select(UserTable).where(UserTable.id == user_id)
        return await self._get_user_table(stmt)

    async def get_user_by_phone(self, *, phone: str) -> User | None:
        stmt = select(UserTable).where(UserTable.phone == phone)
        return await self._get_user_table(stmt)

    async def save_user(self, *, user: User) -> User:
        now = datetime.now(tz=timezone.utc)
        user_row = dict(
            account=user.account,
            phone=user.phone,
            birth=user.birth,
            verified_at=user.verified_at,
            created_at=now,
        )
        stmt = insert(UserTable).values(**user_row).on_duplicate_key_update(**user_row)
        result = await self.session.execute(stmt)
        user.id, *_ = result.inserted_primary_key_rows
        return user

    async def save_certification(
        self,
        *,
        user_id: int,
        certification_type: CertificationType,
        certification: CertificationInfo,
    ):
        now = datetime.now(tz=timezone.utc)
        cert_row = CertificationTable(
            user_id=user_id,
            certification_type=certification_type,
            name=certification.name,
            gender=certification.gender,
            birth=certification.birth,
            unique_key=certification.unique_key,
            unique_in_site=certification.unique_in_site,
            created_at=now,
        )
        self.session.add(cert_row)
