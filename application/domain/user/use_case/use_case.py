from datetime import date

from application.domain.authentication.model import UserData
from application.domain.user.error import AccountIsDuplicated, CertificationIsWrong
from application.domain.user.model import User
from application.domain.user.model.certification_info import GUARDIAN_Certification, SELF_Certification
from application.domain.user.model.vo import PreSignedUrl
from application.domain.user.use_case.port.input import UserInputPort
from application.domain.user.use_case.port.output import (
    AuthenticationOutputPort,
    CertificationOutputPort,
    UserS3OutputPort,
    UserStoreOutputPort,
)
from application.error import NotFound


class UserUseCase(UserInputPort):
    def __init__(
        self,
        *,
        user_store: UserStoreOutputPort,
        auth_app: AuthenticationOutputPort,
        certification_app: CertificationOutputPort,
        s3_app: UserS3OutputPort,
    ):
        self.user_store = user_store
        self.auth_app = auth_app
        self.cert_app = certification_app
        self.s3_app = s3_app

    async def create_user_with_password(
        self,
        *,
        account: str,
        phone: str,
        password: str,
        birth: date,
    ) -> User:
        async with self.user_store as uow:
            if await uow.get_user_by_account(account=account):
                raise AccountIsDuplicated(f"account: {account} is duplicated")
            user = User(account=account, birth=birth, phone=phone)
            await uow.save_user(user=user)
            assert user.id is not None
            await self.auth_app.create_user_password_authenticator(
                user_data=UserData(id=user.id, account=user.account),
                password=password,
            )
            await uow.commit()
            return user

    async def check_account(self, *, account: str) -> bool:
        async with self.user_store(read_only=True) as uow:
            user = await uow.get_user_by_account(account=account)
            return user is not None

    async def get_user_by_user_id(self, *, user_id: int) -> User:
        async with self.user_store(read_only=True) as uow:
            user = await uow.get_user_by_user_id(user_id=user_id)
            if user is None:
                raise NotFound(f"user not found, {user_id=}")
            return user

    async def get_user_by_phone(self, *, phone: str) -> User:
        async with self.user_store(read_only=True) as uow:
            user = await uow.get_user_by_phone(phone=phone)
            if user is None:
                raise NotFound(f"user not found, {phone=}")
            return user

    async def certificate_self(self, *, user_id: int, imp_uid: str):
        async with self.user_store(read_only=True) as uow:
            user = await uow.get_user_by_user_id(user_id=user_id)
            if user is None:
                raise NotFound(f"user not exist, {user_id=}")

        certification_info = await self.cert_app.get_certification_info(imp_uid=imp_uid)
        if certification_info is None:
            raise CertificationIsWrong(f"wrong imp_uid, {imp_uid=}")

        user.verify_self(certification=certification_info)
        async with self.user_store() as uow:
            await uow.save_certification(
                user_id=user_id,
                certification_type=SELF_Certification,
                certification=certification_info,
            )
            await uow.save_user(user=user)
            await uow.commit()

    async def certificate_guardian(self, *, user_id: int, imp_uid: str):
        async with self.user_store(read_only=True) as uow:
            user = await uow.get_user_by_user_id(user_id=user_id)
            if user is None:
                raise NotFound(f"user not exist, {user_id=}")

        certification_info = await self.cert_app.get_certification_info(imp_uid=imp_uid)
        if certification_info is None:
            raise CertificationIsWrong(f"wrong imp_uid, {imp_uid=}")

        user.verify_guardian(certification=certification_info)

        async with self.user_store() as uow:
            await uow.save_certification(
                user_id=user_id,
                certification_type=GUARDIAN_Certification,
                certification=certification_info,
            )
            await uow.commit()

    async def agree_terms(self, *, user_id: int, agree_marketing: bool, agree_push: bool):
        async with self.user_store() as uow:
            user = await uow.get_user_by_user_id(user_id=user_id)
            if user is None:
                raise NotFound(f"user not exist, {user_id=}")

            user.agree_service_policy()
            user.agree_privacy_policy()
            if agree_marketing:
                user.agree_marketing_policy()
            else:
                user.disagree_marketing_policy()
            if agree_push:
                user.agree_push()
            else:
                user.disagree_push()
            await uow.save_user(user=user)
            await uow.commit()

    async def get_face_video_upload_url(self, *, user_id: int) -> PreSignedUrl:
        async with self.user_store(read_only=True) as uow:
            user = await uow.get_user_by_user_id(user_id=user_id)
            if user is None:
                raise NotFound(f"user not exist, {user_id=}")

            return await self.s3_app.make_face_upload_pre_signed_url(user_id=user_id)

    async def request_verifying_face(self, *, user_id: int, face_vide_s3_key: str):
        async with self.user_store() as uow:
            user = await uow.get_user_by_user_id(user_id=user_id)
            if user is None:
                raise NotFound(f"user not exist, {user_id=}")

            # TODO: 기존에 진행중인 얼굴인증 요청이 있다면 새로 생성하지 못하도록 변경
            request = user.request_face_verification(
                face_video_s3_key=face_vide_s3_key,
            )
            await uow.save_face_verification_request(face_verification_request=request)
            await uow.commit()
