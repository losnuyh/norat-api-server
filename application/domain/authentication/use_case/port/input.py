from abc import ABC, abstractmethod

from application.domain.authentication.model import AuthToken, PhoneToken, UserData


class AuthenticationInputPort(ABC):
    @abstractmethod
    async def send_verification_code_to_phone(self, *, phone_number: str) -> None:
        ...

    @abstractmethod
    async def get_phone_verification_token(self, *, phone: str, code: str) -> PhoneToken:
        ...

    @abstractmethod
    async def create_user_password_authenticator(self, *, user_data: UserData, password: str):
        ...

    @abstractmethod
    async def login_user_with_password(self, *, account: str, password: str) -> AuthToken:
        ...

    @abstractmethod
    async def refresh_user_token(self, *, user_id: int, refresh_token: str) -> AuthToken:
        ...
