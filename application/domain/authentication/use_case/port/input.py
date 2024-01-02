from abc import ABC, abstractmethod

from application.domain.authentication.model import PhoneToken


class AuthenticationInputPort(ABC):
    @abstractmethod
    async def send_verification_code_to_phone(self, *, phone_number: str) -> None:
        ...

    @abstractmethod
    async def get_phone_verification_token(self, *, phone: str, code: str) -> PhoneToken:
        ...
