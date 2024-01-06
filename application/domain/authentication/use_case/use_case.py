from datetime import datetime, timedelta, timezone
from random import choices

from application.domain.authentication.error import AuthenticationFail
from application.domain.authentication.model import AuthenticationPhone, PhoneToken
from application.domain.authentication.use_case.port.input import AuthenticationInputPort
from application.domain.authentication.use_case.port.output import AuthenticationStoreOutputPort, CodeSenderOutputPort


class AuthenticationUseCase(AuthenticationInputPort):
    def __init__(self, *, code_sender: CodeSenderOutputPort, auth_store: AuthenticationStoreOutputPort):
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
            await self.code_sender.send_code(
                authentication_phone=authentication_phone,
            )  # TODO: send 실패한 경우 commit하지 않을 할 수 있게 개선
            await uow.commit()

    async def get_phone_verification_token(self, *, phone: str, code: str) -> PhoneToken:
        async with self.auth_store(read_only=True) as uow:
            authentication_phone = await uow.get_authentication_phone(phone=phone)
            if authentication_phone is None:
                raise AuthenticationFail("authentication is not in progress")
            token = authentication_phone.get_token(code=code)
            return token
