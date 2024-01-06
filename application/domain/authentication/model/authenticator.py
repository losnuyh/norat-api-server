from dataclasses import dataclass

import bcrypt

from application.domain.authentication.error import PasswordNotMatched, PasswordValidationFail
from application.jwt import jwt_token_manager

from .token import AuthToken


@dataclass
class PasswordAuthenticator:
    user_id: int
    user_account: str
    hashed_password: bytes

    def _check_password(self, *, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(),
            self.hashed_password,
        )


@dataclass
class PasswordValidator:
    raw_password: str

    @staticmethod
    def _validate_password(password: str):
        if len(password) < 8 | len(password) > 32:
            raise PasswordValidationFail("password length must be greater than 8 and less than 32")

    def __post_init__(self):
        self._validate_password(self.raw_password)

    def new_password_authenticator(
        self,
        *,
        user_id: int,
        user_account: str,
    user_password: str,
    ) -> PasswordAuthenticator:
        hashed_password = bcrypt.hashpw(
            self.raw_password.encode(),
            bcrypt.gensalt(14),
        )
        return PasswordAuthenticator(
            user_id=user_id,
            user_account=user_account,
            hashed_password=hashed_password,
        )
