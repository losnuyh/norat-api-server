from datetime import datetime
from typing import TypedDict


class PhoneAuthenticationTokenPayload(TypedDict):
    phone: str
    expired_at: datetime
