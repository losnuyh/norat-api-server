from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select

from application.domain.authentication.model import AuthenticationPhone, PasswordAuthenticator
from application.domain.authentication.use_case.port.output import AuthenticationStoreOutputPort

from .table import AuthPhoneTable, PasswordAuthenticatorTable


class AuthenticationStoreAdaptor(AuthenticationStoreOutputPort):
    async def save_auth_phone(self, *, authentication_phone: AuthenticationPhone):
        item = AuthPhoneTable(
            code=authentication_phone.code,
            expired_at=authentication_phone.expired_at.astimezone(tz=timezone.utc),
            phone=authentication_phone.phone,
            created_at=datetime.now(tz=timezone.utc),
        )
        self.session.add(item)

    async def get_authentication_phone(self, *, phone: str) -> AuthenticationPhone | None:
        stmt = select(AuthPhoneTable).where(AuthPhoneTable.phone == phone).order_by(-AuthPhoneTable.id).limit(1)
        data: AuthPhoneTable = await self.session.scalar(stmt)
        if data is None:
            return None
        return AuthenticationPhone(
            code=data.code,
            phone=data.phone,
            expired_at=data.expired_at.replace(tzinfo=timezone.utc),
        )

    async def save_user_password_authenticator(self, *, password_authenticator: PasswordAuthenticator):
        item = PasswordAuthenticatorTable(
            user_account=password_authenticator.user_account,
            hashed_password=password_authenticator.hashed_password,
            updated_at=datetime.now(tz=timezone.utc),
        )
        self.session.add(item)
