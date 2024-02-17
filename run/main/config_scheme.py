from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationConfigScheme:
    NEIS_KEY: str
