from abc import ABC, abstractmethod
from datetime import date

from application.domain.authentication.model import AuthToken, PhoneToken
from application.domain.user.model import User


class AuthenticationInputPort(ABC):
    @abstractmethod
    async def send_verification_code_to_phone(self, *, phone_number: str) -> None:
        ...

    @abstractmethod
    async def get_phone_verification_token(self, *, phone: str, code: str) -> PhoneToken:
        ...

    @abstractmethod
    async def create_user_with_password(self, *, password: str, account: str, birth: date) -> User:
        ...

    @abstractmethod
    async def login_user_with_password(self, *, account: str, password: str) -> AuthToken:
        ...
