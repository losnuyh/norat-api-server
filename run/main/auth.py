from typing import Annotated, Tuple

from fastapi import Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from common.util.token.jwt import jwt_token_manager
from common.util.token.jwt.token_type import PhoneAuthenticationTokenPayload, UserAuthenticationTokenPayload

oauth2_scheme = HTTPBearer()

oauth2_phone_or_user_scheme = HTTPBearer()


def get_authenticated_phone_or_user(
    token: Annotated[
        HTTPAuthorizationCredentials,
        Depends(oauth2_phone_or_user_scheme),
    ],
) -> Tuple[str, str | int | None]:
    phone: str | None = None
    user_id: int | None = None
    try:
        phone_payload: PhoneAuthenticationTokenPayload = jwt_token_manager.get_phone_authentication_payload(
            jwt_token=token.credentials,
        )
        phone = phone_payload["phone"]
    except InvalidTokenError:
        pass
    try:
        user_payload: UserAuthenticationTokenPayload = jwt_token_manager.get_user_authentication_payload(
            jwt_token=token.credentials,
        )
        user_id = user_payload["user_id"]
    except InvalidTokenError:
        pass
    if phone is None and user_id is None:
        raise InvalidTokenError

    # User_id is determined first
    if user_id is not None:
        return "user_id", user_id
    return "phone", phone


def get_authenticated_phone(
    token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
) -> str | None:
    payload = jwt_token_manager.get_phone_authentication_payload(
        jwt_token=token.credentials,
    )
    return payload["phone"]


def get_authenticated_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    verify_exp: Annotated[bool, Query(include_in_schema=False)] = True,
) -> int | None:
    payload = jwt_token_manager.get_user_authentication_payload(jwt_token=token.credentials, verify_exp=verify_exp)
    return payload["user_id"]
