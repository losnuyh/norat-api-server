from abc import ABC, abstractmethod

from application.domain.authentication.model import AuthenticationPhone
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
