from typing import Protocol

from application.domain.user.model import FaceVerificationStatus


class UserOutputPort(Protocol):
    async def change_user_face_verification(self, *, verification_request_id: int, status: FaceVerificationStatus):
        ...
