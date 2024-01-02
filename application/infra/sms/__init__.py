from abc import ABC, abstractmethod


class SMSSender(ABC):
    @abstractmethod
    async def send_message(
        self,
        *,
        phone: str,
        message: str,
    ):
        ...
