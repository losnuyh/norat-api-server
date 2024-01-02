from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from application.domain.authentication.model import AuthenticationPhone
from application.domain.authentication.use_case.port.output import AuthenticationStoreOutputPort

from .table import AuthPhoneTable


class AuthenticationStoreAdaptor(AuthenticationStoreOutputPort):
    def __init__(self, *, engine: AsyncEngine, readonly_engine: AsyncEngine):
        self.engine = engine
        self.readonly_engine = readonly_engine

    async def save_auth_phone(self, *, authentication_phone: AuthenticationPhone):
        async with AsyncSession(self.engine) as session:
            item = AuthPhoneTable(
                code=authentication_phone.code,
                expired_at=authentication_phone.expired_at.astimezone(tz=timezone.utc),
                phone=authentication_phone.phone,
                created_at=datetime.now(tz=timezone.utc),
            )
            session.add(item)
            await session.commit()

    async def get_authentication_phone(self, *, phone: str) -> AuthenticationPhone | None:
        async with AsyncSession(self.readonly_engine) as session:
            stmt = select(AuthPhoneTable).where(AuthPhoneTable.phone == phone).order_by(-AuthPhoneTable.id).limit(1)
            data: AuthPhoneTable = await session.scalar(stmt)
            if data is None:
                return None
            return AuthenticationPhone(
                code=data.code,
                phone=data.phone,
                expired_at=data.expired_at.replace(tzinfo=timezone.utc),
            )
