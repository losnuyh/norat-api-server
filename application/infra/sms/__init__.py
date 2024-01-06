from abc import ABC, abstractmethod


class SendFail(Exception):
    ...


class SMSSender(ABC):
    @abstractmethod
    async def send_message(
        self,
        *,
        phone: str,
        message: str,
    ):
        ...
