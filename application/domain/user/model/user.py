from dataclasses import dataclass
from datetime import date, datetime, timezone

from application.domain.user.error import CertificationIsWrong
from application.error import InvalidData

from .certification_info import CertificationInfo


@dataclass(kw_only=True)
class User:
    id: int | None = None
    account: str
    phone: str
    birth: date
    verified_at: datetime | None = None

    @property
    def age(self):
        current_year = datetime.now().year
        birth_year = self.birth.year
        return current_year - birth_year

    def verify_self(self, *, certification: CertificationInfo):
        if self.age < 14:
            raise InvalidData(f"wrong user age: {self.age=}")

        if self.birth != certification.birth:
            raise CertificationIsWrong(f"not matched, {self.birth=}, {certification.birth=}")
        # TODO: name 저장 ?
        self.verified_at = datetime.now(tz=timezone.utc)

    def verify_guardian(self, *, certification: CertificationInfo):
        if self.age >= 14:
            raise InvalidData(f"wrong user age: {self.age=}")

        if certification.age < 20:
            raise CertificationIsWrong(f"wrong guardian age: {certification.age=}")
        self.verified_at = datetime.now(tz=timezone.utc)
