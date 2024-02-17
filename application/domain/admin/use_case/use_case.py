from application.domain.admin.use_case.port.input import AdminInputPort
from application.domain.admin.use_case.port.output import UserOutputPort
from application.domain.user.model import FaceVerificationStatus


class AdminUseCase(AdminInputPort):
    def __init__(self, *, user_output: UserOutputPort):
        self.user_app = user_output

    async def change_user_face_verification_request_status(
        self,
        *,
        face_verification_request_id: int,
        status: FaceVerificationStatus,
    ):
        # 어드민 로깅
        await self.user_app.change_user_face_verification(
            verification_request_id=face_verification_request_id,
            status=status,
        )
