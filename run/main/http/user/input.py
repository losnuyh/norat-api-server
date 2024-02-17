from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from application.domain.user.model import User
from application.domain.user.use_case.port.input import UserInputPort
from application.error import PermissionDenied
from application.infra.fastapi import WithFastAPIRouter
from run.main.auth import get_authenticated_phone, get_authenticated_phone_or_user, get_authenticated_user

from .dto import (
    AgreeTermsRequest,
    CertificationRequest,
    CheckUserAccountDuplicationResponse,
    GetLastFaceVerificationRequestResponse,
    PreSignedUrlResponse,
    RequestFaceVerificationRequest,
    UserResponse,
    UserSignupRequest,
    UserSignupResponse,
)

user_router = APIRouter()


class UserHttpInputAdaptor(WithFastAPIRouter):
    def __init__(self, *, input: UserInputPort):
        self.input = input

    def check_account_duplication(self):
        @user_router.get(
            path="/check",
            tags=["user"],
            summary="아이디 중복 체크",
            status_code=status.HTTP_200_OK,
            response_description="아이디 중복 여부를 확인합니다.",
            responses={
                status.HTTP_200_OK: {"model": CheckUserAccountDuplicationResponse, "description": "유저 아이디 중복 체크 결과"},
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(account: Annotated[str, Query()]):
            is_exist = await self.input.check_account(account=account)
            return CheckUserAccountDuplicationResponse(
                account=account,
                is_exist=is_exist,
            )

    def signup(self):
        @user_router.post(
            path="",
            tags=["user"],
            summary="회원 가입",
            description="</br>".join(["회원가입 합니다.", "가입 요칭시 phone 인증 토큰을 필요로 합니다."]),
            status_code=status.HTTP_200_OK,
            response_description="유저 정보",
            responses={
                status.HTTP_200_OK: {
                    "model": UserSignupResponse,
                    "description": "가입 성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            phone: Annotated[str, Depends(get_authenticated_phone)],
            body: Annotated[UserSignupRequest, Body()],
        ):
            user = await self.input.create_user_with_password(
                password=body.password,
                account=body.account,
                phone=phone,
                birth=body.birth,
            )
            assert user.id is not None
            return UserSignupResponse(
                id=user.id,
                account=user.account,
                birth=user.birth,
            )

    def certificate_self(self):
        @user_router.post(
            path="/{user_id}/certification/self",
            tags=["user"],
            summary="본인 인증 완료 요청",
            description="</br>".join(
                [
                    "포트원 본인인증 완료 후, 인증 완료 처리를 서버에 요청합니다.",
                    "포트원 본인인증 후 받은 imp_uid를 전송합니다.",
                    "본인 인증인 경우에만 가능합니다. 부모 인증은 허용하지 않습니다.",
                    "가입시 입력한 정보가 14세 미만인 경우에는 본인인증 api를 호출할 수 없습니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            body: Annotated[CertificationRequest, Body()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            await self.input.certificate_self(user_id=user_id, imp_uid=body.imp_uid)
            return {"message": "success"}

    def certificate_guardian(self):
        @user_router.post(
            path="/{user_id}/certification/guardian",
            tags=["user"],
            summary="보호자 인증 완료 요청",
            description="</br>".join(
                [
                    "포트원 보호자 완료 후, 인증 완료 처리를 서버에 요청합니다.",
                    "포트원 보호자 후 받은 imp_uid를 전송합니다.",
                    "보호자 인증인 경우에만 가능합니다.",
                    "가입시 입력한 정보가 14세 이상인 경우에는 보호자인증 api를 호출할 수 없습니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            body: Annotated[CertificationRequest, Body()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            await self.input.certificate_guardian(user_id=user_id, imp_uid=body.imp_uid)
            return {"message": "success"}

    def get_my_info(self):
        @user_router.post(
            path="/me",
            tags=["user"],
            summary="내 정보 가져오기",
            description="</br>".join(
                [
                    "내 계정 정보를 받아옵니다.",
                    "phone token 또는 auth token으로 접근할 수 있습니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "model": UserResponse,
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            authenticated: Annotated[tuple, Depends(get_authenticated_phone_or_user)],
        ):
            authenticated_entity, value = authenticated
            user: User | None = None
            match authenticated_entity:
                case "phone":
                    user = await self.input.get_user_by_phone(phone=value)
                case "user_id":
                    user = await self.input.get_user_by_user_id(user_id=value)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="user not found",
                )
            assert user.id is not None
            return UserResponse(
                id=user.id,
                account=user.account,
                birth=user.birth,
                verified_at=user.verified_at,
                privacy_policy_agreed_at=user.privacy_policy_agreed_at,
                terms_policy_agreed_at=user.service_policy_agreed_at,
                marketing_policy_agreed_at=user.marketing_policy_agreed_at,
                push_agreed_at=user.push_agreed_at,
            )

    def agree_terms(self):
        @user_router.post(
            path="/{user_id}/terms",
            tags=["user", "terms"],
            summary="약관 동의하기",
            description="</br>".join(
                [
                    "약관 동의 정보를 기록합니다.",
                    "선택 약관 정보만 받습니다. 필수 약관은 요청 시점으로 동의로 간주합니다.",
                    "선택 약관은 false <-> true로 변경할 수 있습니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            body: Annotated[AgreeTermsRequest, Body()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            await self.input.agree_terms(
                user_id=user_id,
                agree_marketing=body.marketing,
                agree_push=body.push,
            )
            return {"message": "success"}

    def get_face_verification_pre_signed_url(self):
        @user_router.get(
            path="/{user_id}/face-verification/pre-signed-url",
            tags=["user"],
            summary="얼굴 인증 동영상 업로드용 url 획득",
            description="</br>".join(
                [
                    "얼굴 인증 동영상 업로드용 url 획득",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            result = await self.input.get_face_video_upload_url(
                user_id=user_id,
            )
            return PreSignedUrlResponse(
                pre_signed_url=result.pre_signed_url,
                key=result.key,
            )

    def request_face_verification(self):
        @user_router.post(
            path="/{user_id}/face-verification",
            tags=["user", "face verification"],
            summary="얼굴 인증 요청",
            description="</br>".join(
                [
                    "얼굴 영상을 업로드한 이후 업로드한 영상의 s3 key와 함께 얼굴 인증을 요청합니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
            body: Annotated[RequestFaceVerificationRequest, Body()],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            await self.input.request_verifying_face(
                user_id=user_id,
                face_vide_s3_key=body.key,
            )
            return {
                "message": "success",
            }

    def get_last_face_verification(self):
        @user_router.get(
            path="/{user_id}/face-verification/last",
            tags=["user", "face verification"],
            summary="최근 얼굴 인증 요청 상태 확인",
            description="</br>".join(
                [
                    "최근에 요청한 얼굴 인증의 처리 상태를 확인합니다.",
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "model": GetLastFaceVerificationRequestResponse,
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            result = await self.input.get_user_last_face_verification(
                user_id=user_id,
            )
            return GetLastFaceVerificationRequestResponse(
                requested_at=result.requested_at,
                changed_at=result.changed_at,
                status=result.status,
            )

    def withdraw_user(self):
        @user_router.delete(
            path="/{user_id}",
            tags=["user"],
            summary="회원 탈퇴",
            description="</br>".join(
                [
                    "회원정보를 제거합니다.",
                    "유저 데이터는 복구할 수 없습니다.",
                    "[개선 예정] 학교 맴버 카운터는 줄어들지 않습니다.",  # TODO: 개선 후에 제거
                ],
            ),
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "description": "성공",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "잘못된 요청",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "찾을 수 없는 정보",
                },
            },
        )
        async def handler(
            user_id: Annotated[int, Path()],
            request_user_id: Annotated[int, Depends(get_authenticated_user)],
        ):
            if user_id != request_user_id:
                raise PermissionDenied("Not permitted")

            await self.input.withdraw_user(
                user_id=user_id,
            )
            return {"message": "success"}
