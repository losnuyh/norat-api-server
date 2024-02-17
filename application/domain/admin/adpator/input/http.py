from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path

from application.domain.admin.use_case.port.input import AdminInputPort
from application.infra.fastapi import WithFastAPIRouter
# from run.admin.auth import check_admin_token

from .dto import ChangeUserFaceVerificationStatusRequest

admin_router = APIRouter()


class AdminHttpInputAdaptor(WithFastAPIRouter):
    def __init__(self, *, input: AdminInputPort):
        self.input = input

    def change_user_face_verification_request_status(self):
        @admin_router.put(
            path="/face_verification/{verification_request_id}/status",
            tags=["admin", "user", "face verification"],
            summary="얼굴 인증 상태 변경",
        )
        async def handler(
            verification_request_id: Annotated[int, Path()],
            body: Annotated[ChangeUserFaceVerificationStatusRequest, Body()],
            # _: Annotated[str, Depends(check_admin_token)],
        ):
            await self.input.change_user_face_verification_request_status(
                face_verification_request_id=verification_request_id,
                status=body.status,
            )
            return {"message": "success"}
