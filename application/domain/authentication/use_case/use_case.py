from datetime import datetime, timedelta, timezone
from random import choices

from application.domain.authentication.error import AuthenticationFail
from application.domain.authentication.model import (
    AuthenticationPhone,
    AuthToken,
    PhoneToken,
    new_password_authenticator,
)
from application.domain.authentication.use_case.port.input import AuthenticationInputPort, UserData
from application.domain.authentication.use_case.port.output import AuthenticationStoreOutputPort, CodeSenderOutputPort
from application.error import NotFound


class AuthenticationUseCase(AuthenticationInputPort):
    def __init__(
        self,
        *,
        code_sender: CodeSenderOutputPort,
        auth_store: AuthenticationStoreOutputPort,
    ):
        self.code_sender = code_sender
        self.auth_store = auth_store

    async def send_verification_code_to_phone(self, *, phone_number: str) -> None:
        authentication_phone = AuthenticationPhone(
            phone=phone_number,
            code="".join(choices("0123456789", k=5)),
            expired_at=datetime.now(tz=timezone.utc) + timedelta(minutes=10),
        )
        async with self.auth_store as uow:
            await uow.save_auth_phone(authentication_phone=authentication_phone)
            is_success = await self.code_sender.send_code(
                authentication_phone=authentication_phone,
            )
            if is_success:
                await uow.commit()
            else:
                await uow.rollback()

    async def get_phone_verification_token(self, *, phone: str, code: str) -> PhoneToken:
        async with self.auth_store(read_only=True) as uow:
            authentication_phone = await uow.get_authentication_phone(phone=phone)
            if authentication_phone is None:
                raise AuthenticationFail("authentication is not in progress")
            token = authentication_phone.get_token(code=code)
            return token

    async def create_user_password_authenticator(self, *, user_data: UserData, password: str):
        async with self.auth_store as uow:
            password_authenticator = new_password_authenticator(
                user_id=user_data.id,
                user_account=user_data.account,
                password=password,
            )
            await uow.save_user_password_authenticator(password_authenticator=password_authenticator)
            await uow.commit()

    async def login_user_with_password(self, *, account: str, password: str) -> AuthToken:
        async with self.auth_store(read_only=True) as uow:
            password_authenticator = await uow.get_user_password_authenticator_by_user_account(account=account)
            if password_authenticator is None:
                raise NotFound("user not found")
            return password_authenticator.get_token_by_password(password=password)

    async def refresh_user_token(self, *, user_id: int, refresh_token: str) -> AuthToken:
        async with self.auth_store(read_only=True) as uow:
            password_authenticator = await uow.get_user_password_authenticator_by_user_id(user_id=user_id)
            if password_authenticator is None:
                raise AuthenticationFail("authentication not found")

            if password_authenticator.refresh_token_expired_at < datetime.now(tz=timezone.utc):
                raise AuthenticationFail("refresh token is expired")

            return password_authenticator.get_token_by_refresh_token(refresh_token=refresh_token)

    async def change_password(self, *, user_id: int, password: str, new_password: str):
        async with self.auth_store() as uow:
            password_authenticator = await uow.get_user_password_authenticator_by_user_id(user_id=user_id)
            if password_authenticator is None:
                raise AuthenticationFail("authentication not found")

            password_authenticator.change_password(password=password, new_password=new_password)
            await uow.save_user_password_authenticator(password_authenticator=password_authenticator)
            await uow.commit()

    async def delete_authenticators(self, *, user_id: int):
        async with self.auth_store() as uow:
            password_authenticator = await uow.get_user_password_authenticator_by_user_id(user_id=user_id)
            if password_authenticator is None:
                raise AuthenticationFail("authentication not found")

            await uow.delete_password_authenticator(password_authenticator=password_authenticator)
            await uow.commit()
