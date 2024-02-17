from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AdminConfigScheme:
    ADMIN_TOKEN: str
