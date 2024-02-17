from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommonConfigScheme:
    JWT_SIGNING_PRIVATE_KEY: str
