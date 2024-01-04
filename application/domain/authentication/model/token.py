from dataclasses import dataclass


@dataclass(kw_only=True)
class PhoneToken:
    access_token: str


@dataclass(kw_only=True)
class AuthToken:
    access_token: str
    refresh_token: str
