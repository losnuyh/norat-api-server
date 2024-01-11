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

    privacy_policy_agreed_at: datetime | None = None
    service_policy_agreed_at: datetime | None = None
    marketing_policy_agreed_at: datetime | None = None
    push_agreed_at: datetime | None = None

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

        self.verified_at = datetime.now(tz=timezone.utc)

    def verify_guardian(self, *, certification: CertificationInfo):
        if self.age >= 14:
            raise InvalidData(f"wrong user age: {self.age=}")

        if certification.age < 20:
            raise CertificationIsWrong(f"wrong guardian age: {certification.age=}")
        self.verified_at = datetime.now(tz=timezone.utc)

    def agree_privacy_policy(self):
        if self.privacy_policy_agreed_at is None:
            self.privacy_policy_agreed_at = datetime.now(tz=timezone.utc)

    def agree_service_policy(self):
        if self.service_policy_agreed_at is None:
            self.service_policy_agreed_at = datetime.now(tz=timezone.utc)

    def agree_marketing_policy(self):
        if self.marketing_policy_agreed_at is None:
            self.marketing_policy_agreed_at = datetime.now(tz=timezone.utc)

    def disagree_marketing_policy(self):
        if self.marketing_policy_agreed_at is not None:
            self.marketing_policy_agreed_at = None

    def agree_push(self):
        if self.push_agreed_at is None:
            self.push_agreed_at = datetime.now(tz=timezone.utc)

    def disagree_push(self):
        if self.push_agreed_at is not None:
            self.push_agreed_at = None
