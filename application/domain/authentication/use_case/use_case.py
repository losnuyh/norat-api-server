from datetime import date, datetime, timedelta, timezone
from random import choices

from application.domain.authentication.error import AuthenticationFail
from application.domain.authentication.model import AuthenticationPhone, PhoneToken, new_password_authenticator
from application.domain.authentication.use_case.port.input import AuthenticationInputPort
from application.domain.authentication.use_case.port.output import (
    AuthenticationStoreOutputPort,
    CodeSenderOutputPort,
    UserOutputPort,
)
from application.domain.user.model import User


class AuthenticationUseCase(AuthenticationInputPort):
    def __init__(
        self,
        *,
        code_sender: CodeSenderOutputPort,
        auth_store: AuthenticationStoreOutputPort,
        user_app: UserOutputPort,
    ):
        self.code_sender = code_sender
        self.auth_store = auth_store
        self.user_app = user_app

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

    async def create_user_with_password(self, *, password: str, account: str, birth: date) -> User:
        password_authenticator = new_password_authenticator(
            user_account=account,
            user_password=password,
        )
        user = await self.user_app.create_user(account=account, birth=birth)
        async with self.auth_store as uow:
            await uow.save_user_password_authenticator(password_authenticator=password_authenticator)
            await uow.commit()
        return user
