from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.jwt import jwt_token_manager

oauth2_scheme = HTTPBearer()

oauth2_phone_or_user_scheme = HTTPBearer()


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
