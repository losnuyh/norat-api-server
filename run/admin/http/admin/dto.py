from pydantic import BaseModel

from application.domain.user.model.face_verification_request import FaceVerificationStatus


class ChangeUserFaceVerificationStatusRequest(BaseModel):
    status: FaceVerificationStatus
