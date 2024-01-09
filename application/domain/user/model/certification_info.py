from dataclasses import dataclass
from datetime import date


@dataclass
class CertificationInfo:
    name: str
    gender: str
    birth: date
    unique_key: str
    unique_in_site: str
