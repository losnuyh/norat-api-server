from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Admin:
    id: int | None = field(default=None)
    account: str
    name: str
