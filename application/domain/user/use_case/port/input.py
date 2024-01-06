from abc import ABC, abstractmethod
from datetime import date

from application.domain.user.model import User


class UserInputPort(ABC):
    @abstractmethod
    async def create_user(self, *, account: str, birth: date) -> User:
        ...

    @abstractmethod
    async def check_account(self, *, account: str) -> bool:
        ...
