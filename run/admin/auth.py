from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette import status

from run.admin.config import app_config

admin_token_Header = APIKeyHeader(
    name="AdminToken",
    scheme_name="AdminToken",
    auto_error=False,
)


def check_admin_token(
    token: str = Security(admin_token_Header),
) -> str:
    if token != app_config.ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authenticated admin",
        )
    return token
