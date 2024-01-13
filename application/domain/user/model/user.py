from dataclasses import dataclass
from datetime import date, datetime, timezone

from application.domain.user.error import AlreadyFaceVerified, CertificationIsWrong
from application.error import InvalidData

from .certification_info import CertificationInfo
from .face_verification_request import FaceVerificationRequest, FaceVerificationStatus


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

    face_verified_at: datetime | None = None

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

    def request_face_verification(self, *, face_video_s3_key: str) -> FaceVerificationRequest:
        if self.face_verified_at is not None:
            raise AlreadyFaceVerified(f"user_id={self.id} already face verified")
        now = datetime.now(tz=timezone.utc)
        assert self.id is not None
        return FaceVerificationRequest(
            user_id=self.id,
            s3_key=face_video_s3_key,
            status=FaceVerificationStatus.IN_PROGRESS,
            requested_at=now,
            changed_at=now,
        )
