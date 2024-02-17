from datetime import datetime, timezone

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from jwt.exceptions import DecodeError, InvalidTokenError

from common.util.token.jwt.token_type import PhoneAuthenticationTokenPayload, UserAuthenticationTokenPayload


class JwtTokenManager:
    def __init__(self, private_key: str):
        self._private_key = load_pem_private_key(
            data=private_key.encode(),
            password=None,
            backend=default_backend(),
        )
        self._public_key = self._private_key.public_key()

    def _create_jwt(self, *, payload: dict) -> str:
        return jwt.encode(payload=payload, key=self._private_key, algorithm="EdDSA")

    def _get_payload(self, *, jwt_token: str, verify_exp: bool = True) -> dict:
        try:
            return jwt.decode(
                jwt=jwt_token,
                key=self._public_key,
                algorithms=["EdDSA"],
                options={"verify_exp": verify_exp},
            )
        except DecodeError:
            raise InvalidTokenError("token is wrong")

    def get_phone_authentication_payload(
        self,
        *,
        jwt_token: str,
    ) -> PhoneAuthenticationTokenPayload:
        payload = self._get_payload(jwt_token=jwt_token)
        try:
            return PhoneAuthenticationTokenPayload(
                phone=payload["phone"],
                expired_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
            )
        except KeyError as e:
            raise InvalidTokenError(f"token is wrong, token payload KeyError: {str(e)}")

    def create_phone_authentication_token(
        self,
        *,
        payload: PhoneAuthenticationTokenPayload,
    ) -> str:
        return self._create_jwt(
            payload={
                "phone": payload["phone"],
                "exp": payload["expired_at"].timestamp(),
            },
        )

    def create_user_authentication_token(
        self,
        *,
        payload: UserAuthenticationTokenPayload,
    ):
        return self._create_jwt(
            payload={
                "user_id": payload["user_id"],
                "exp": payload["expired_at"].timestamp(),
            },
        )

    def get_user_authentication_payload(
        self, *, jwt_token: str, verify_exp: bool = True
    ) -> UserAuthenticationTokenPayload:
        payload = self._get_payload(jwt_token=jwt_token, verify_exp=verify_exp)
        try:
            return UserAuthenticationTokenPayload(
                user_id=payload["user_id"],
                expired_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
            )
        except KeyError as e:
            raise InvalidTokenError(f"token is wrong, token payload KeyError: {str(e)}")
