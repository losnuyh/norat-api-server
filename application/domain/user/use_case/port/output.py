from abc import ABC, abstractmethod
from typing import Protocol

from application.domain.authentication.model import UserData
from application.domain.user.model import CertificationInfo, CertificationType, FaceVerificationRequest, User
from application.domain.user.model.vo import PreSignedUrl
from application.infra.unit_of_work.sqlalchemy import UnitOfWork


class UserS3OutputPort(ABC):
    @abstractmethod
    async def make_face_upload_pre_signed_url(self, *, user_id: int) -> PreSignedUrl:
        ...


class CertificationOutputPort(ABC):
    @abstractmethod
    async def get_certification_info(self, *, imp_uid: str) -> CertificationInfo | None:
        ...


class UserStoreOutputPort(UnitOfWork, ABC):
    @abstractmethod
    async def get_user_by_account(self, *, account: str) -> User | None:
        ...

    @abstractmethod
    async def get_user_by_user_id(self, *, user_id: int) -> User | None:
        ...

    @abstractmethod
    async def get_user_by_phone(self, *, phone: str) -> User | None:
        ...

    @abstractmethod
    async def save_user(self, *, user: User) -> User:
        ...

    @abstractmethod
    async def save_certification(
        self, *, user_id: int, certification_type: CertificationType, certification: CertificationInfo
    ):
        ...

    @abstractmethod
    async def save_face_verification_request(self, *, face_verification_request: FaceVerificationRequest):
        ...

    @abstractmethod
    async def get_user_last_face_verification_request(self, *, user_id: int) -> FaceVerificationRequest | None:
        ...

    @abstractmethod
    async def get_user_face_verification_request(
        self, *, verification_request_id: int
    ) -> FaceVerificationRequest | None:
        ...

    @abstractmethod
    async def delete_user(self, *, user: User):
        ...


class AuthenticationOutputPort(Protocol):
    async def create_user_password_authenticator(self, *, user_data: UserData, password: str):
        ...

    async def delete_authenticators(self, *, user_id: int):
        ...
