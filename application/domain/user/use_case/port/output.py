from abc import ABC, abstractmethod

from application.domain.user.model import User
from application.infra.unit_of_work.sqlalchemy import UnitOfWork


class UserStoreOutputPort(UnitOfWork, ABC):
    @abstractmethod
    async def get_user_by_account(self, *, account: str) -> User | None:
        ...

    @abstractmethod
    async def save_user(self, *, user: User) -> User:
        ...
