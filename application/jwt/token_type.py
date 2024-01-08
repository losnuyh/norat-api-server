from datetime import datetime
from typing import TypedDict


class PhoneAuthenticationTokenPayload(TypedDict):
    phone: str
    expired_at: datetime


class UserAuthenticationTokenPayload(TypedDict):
    user_id: int
    expired_at: datetime
