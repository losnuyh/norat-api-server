from abc import ABC, abstractmethod
from datetime import date
from typing import Protocol

from application.domain.authentication.model import AuthenticationPhone, PasswordAuthenticator
from application.domain.user.model import User
from application.infra.unit_of_work.sqlalchemy import UnitOfWork


class CodeSenderOutputPort(ABC):
    @abstractmethod
    async def send_code(self, *, authentication_phone: AuthenticationPhone) -> bool:
        ...


class AuthenticationStoreOutputPort(UnitOfWork, ABC):
    @abstractmethod
    async def save_auth_phone(self, *, authentication_phone: AuthenticationPhone):
        ...

    @abstractmethod
    async def get_authentication_phone(self, *, phone: str) -> AuthenticationPhone | None:
        ...

    @abstractmethod
    async def save_user_password_authenticator(self, *, password_authenticator: PasswordAuthenticator):
        ...

    @abstractmethod
    async def get_user_password_authenticator_by_user_id(self, *, user_id: int) -> PasswordAuthenticator | None:
        ...

    @abstractmethod
    async def get_user_password_authenticator_by_user_account(self, *, account: str) -> PasswordAuthenticator | None:
        ...

    @abstractmethod
    async def delete_password_authenticator(self, *, password_authenticator: PasswordAuthenticator):
        ...


class UserOutputPort(Protocol):
    async def create_user(self, *, account: str, birth: date) -> User:
        ...
