from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from secrets import token_hex

import bcrypt

from application.domain.authentication.error import AuthenticationFail, PasswordNotMatched, PasswordValidationFail
from application.jwt import jwt_token_manager

from .token import AuthToken


@dataclass
class PasswordAuthenticator:
    user_id: int
    user_account: str
    hashed_password: bytes
    password_update_at: datetime
    refresh_token_expired_at: datetime
    refresh_token: str

    def _check_password(self, *, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(),
            self.hashed_password,
        )

    def _generate_token(self) -> AuthToken:
        now = datetime.now(tz=timezone.utc)
        jwt_token = jwt_token_manager.create_user_authentication_token(
            payload={
                "user_id": self.user_id,
                "expired_at": now + timedelta(minutes=10),
            },
        )
        return AuthToken(
            access_token=jwt_token,
            refresh_token=self.refresh_token,
        )

    def get_token_by_password(self, *, password: str) -> AuthToken:
        if not self._check_password(password=password):
            raise PasswordNotMatched("wrong password")
        return self._generate_token()

    def get_token_by_refresh_token(self, *, refresh_token: str) -> AuthToken:
        if self.refresh_token == refresh_token and self.refresh_token_expired_at >= datetime.now(tz=timezone.utc):
            raise AuthenticationFail("refresh token is not correct")
        return self._generate_token()


def new_password_authenticator(user_id: int, user_account: str, password: str):
    if len(password) < 8 | len(password) > 32:
        raise PasswordValidationFail("password length must be greater than 8 and less than 32")
    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(14),
    )
    now = datetime.now(tz=timezone.utc)
    return PasswordAuthenticator(
        user_id=user_id,
        user_account=user_account,
        hashed_password=hashed_password,
        password_update_at=now,
        refresh_token=token_hex(),
        refresh_token_expired_at=now + timedelta(days=365),
    )
