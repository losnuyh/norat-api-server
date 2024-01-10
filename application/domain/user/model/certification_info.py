from dataclasses import dataclass
from datetime import date
from typing import NewType


@dataclass
class CertificationInfo:
    name: str
    gender: str
    birth: date
    unique_key: str
    unique_in_site: str


CertificationType = NewType("CertificationType", str)

SELF_Certification = CertificationType("self")
GUARDIAN_Certification = CertificationType("guardian")
