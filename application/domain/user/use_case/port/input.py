from abc import ABC, abstractmethod
from datetime import date

from application.domain.user.model import User


class UserInputPort(ABC):
    @abstractmethod
    async def create_user_with_password(
        self,
        *,
        account: str,
        phone: str,
        password: str,
        birth: date,
    ) -> User:
        ...

    @abstractmethod
    async def check_account(self, *, account: str) -> bool:
        ...

    @abstractmethod
    async def certificate_self(self, *, user_id: int, imp_uid: str):
        ...

