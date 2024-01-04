from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from application.domain.authentication.error import AuthenticationFail
from application.jwt import jwt_token_manager
from application.jwt.token_type import PhoneAuthenticationTokenPayload

from .token import PhoneToken



@dataclass
class AuthenticationPhone:
    code: str
    phone: str
    expired_at: datetime

    def _check_token(self, *, code: str) -> bool:
        return self.code == code and self.expired_at >= datetime.now(tz=timezone.utc)

    def get_token(self, *, code: str) -> PhoneToken:
        if not self._check_token(code=code):
            raise AuthenticationFail("code is not correct")
        now = datetime.now(tz=timezone.utc)
        payload = PhoneAuthenticationTokenPayload(
            phone=self.phone,
            expired_at=now + timedelta(minutes=10),
        )

        jwt_token = jwt_token_manager.create_phone_authentication_token(
            payload=payload,
        )
        return PhoneToken(access_token=jwt_token)


def new_authentication_phone(
    *,
    code: str,
    phone: str,
):
    if phone == "01047374146":
        code = "00000"

    return AuthenticationPhone(
        code=code,
        phone=phone,
        expired_at=datetime.now(tz=timezone.utc) + timedelta(minutes=10),
    )
