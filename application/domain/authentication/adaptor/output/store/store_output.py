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
            user_id=password_authenticator.user_id,
            user_account=password_authenticator.user_account,
            hashed_password=password_authenticator.hashed_password,
            password_updated_at=password_authenticator.password_update_at.astimezone(tz=timezone.utc),
            refresh_token=password_authenticator.refresh_token,
            refresh_token_expired_at=password_authenticator.refresh_token_expired_at.astimezone(tz=timezone.utc),
        )
        self.session.add(item)

    async def get_user_password_authenticator_by_user_id(self, *, user_id: int) -> PasswordAuthenticator | None:
        stmt = select(PasswordAuthenticatorTable).where(PasswordAuthenticatorTable.user_id == user_id)
        data: PasswordAuthenticatorTable = await self.session.scalar(stmt)
        if data is None:
            return None
        return PasswordAuthenticator(
            user_id=data.user_id,
            user_account=data.user_account,
            hashed_password=data.hashed_password.encode(),
            password_update_at=data.password_updated_at.replace(tzinfo=timezone.utc),
            refresh_token=data.refresh_token,
            refresh_token_expired_at=data.refresh_token_expired_at.replace(tzinfo=timezone.utc),
        )

    async def get_user_password_authenticator_by_user_account(self, *, account: str) -> PasswordAuthenticator | None:
        stmt = select(PasswordAuthenticatorTable).where(PasswordAuthenticatorTable.user_account == account)
        data: PasswordAuthenticatorTable = await self.session.scalar(stmt)
        if data is None:
            return None
        return PasswordAuthenticator(
            user_id=data.user_id,
            user_account=data.user_account,
            hashed_password=data.hashed_password.encode(),
            password_update_at=data.password_updated_at.replace(tzinfo=timezone.utc),
            refresh_token=data.refresh_token,
            refresh_token_expired_at=data.refresh_token_expired_at.replace(tzinfo=timezone.utc),
        )
