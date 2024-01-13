from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto


class FaceVerificationStatus(StrEnum):
    IN_PROGRESS = auto()
    REJECTED = auto()
    ACCEPTED = auto()


@dataclass
class FaceVerificationRequest:
    user_id: int
    s3_key: str
    status: FaceVerificationStatus
    requested_at: datetime
    changed_at: datetime
    id: int | None = None
