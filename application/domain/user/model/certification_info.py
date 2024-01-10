from dataclasses import dataclass
from datetime import date, datetime
from typing import NewType


@dataclass
class CertificationInfo:
    name: str
    gender: str
    birth: date
    unique_key: str
    unique_in_site: str

    @property
    def age(self):
        current_year = datetime.now().year
        birth_year = self.birth.year
        return current_year - birth_year


CertificationType = NewType("CertificationType", str)

SELF_Certification = CertificationType("self")
GUARDIAN_Certification = CertificationType("guardian")
