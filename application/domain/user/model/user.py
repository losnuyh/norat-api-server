from dataclasses import dataclass
from datetime import date


@dataclass(kw_only=True)
class User:
    id: int | None = None
    account: str
    birth: date
