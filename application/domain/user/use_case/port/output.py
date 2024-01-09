from abc import ABC, abstractmethod
from typing import Protocol

from application.domain.authentication.model import UserData
from application.domain.user.model import CertificationInfo, User
from application.infra.unit_of_work.sqlalchemy import UnitOfWork


class CertificationOutputPort(ABC):
    @abstractmethod
    async def get_certification_info(self, *, imp_uid: str) -> CertificationInfo | None:
        ...


class UserStoreOutputPort(UnitOfWork, ABC):
    @abstractmethod
    async def get_user_by_account(self, *, account: str) -> User | None:
        ...

    @abstractmethod
    async def get_user_by_user_id(self, *, user_id: int) -> User | None:
        ...

    @abstractmethod
    async def save_user(self, *, user: User) -> User:
        ...


class AuthenticationOutputPort(Protocol):
    async def create_user_password_authenticator(self, *, user_data: UserData, password: str):
        ...
