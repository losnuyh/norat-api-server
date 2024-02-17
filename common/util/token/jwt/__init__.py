from common.config import app_config

from .token_manager import JwtTokenManager

jwt_token_manager = JwtTokenManager(
    private_key=app_config.JWT_SIGNING_PRIVATE_KEY,
)
