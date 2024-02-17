from abc import ABC, abstractmethod

from application.domain.user.model.face_verification_request import FaceVerificationStatus


class AdminInputPort(ABC):
    @abstractmethod
    async def change_user_face_verification_request_status(
        self,
        *,
        face_verification_request_id: int,
        status: FaceVerificationStatus,
    ):
        ...
