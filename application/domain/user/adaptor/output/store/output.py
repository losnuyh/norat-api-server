from datetime import datetime, timezone

from sqlalchemy import Select, delete, select
from sqlalchemy.dialects.mysql import insert

from application.domain.user.model import CertificationInfo, CertificationType, FaceVerificationRequest, User
from application.domain.user.use_case.port.output import UserStoreOutputPort

from .table import CertificationTable, FaceVerificationRequestTable, UserTable


class UserStoreAdaptor(UserStoreOutputPort):
    async def _get_user_table(self, select_stmt: Select) -> User | None:
        user_result: UserTable = await self.session.scalar(select_stmt)
        if user_result is None:
            return None
        return User(
            id=user_result.id,
            account=user_result.account,
            phone=user_result.phone,
            birth=user_result.birth,
            verified_at=user_result.verified_at
            and user_result.verified_at.replace(
                tzinfo=timezone.utc,
            ),
            privacy_policy_agreed_at=user_result.privacy_policy_agreed_at
            and user_result.privacy_policy_agreed_at.replace(
                tzinfo=timezone.utc,
            ),
            service_policy_agreed_at=user_result.service_policy_agreed_at
            and user_result.service_policy_agreed_at.replace(
                tzinfo=timezone.utc,
            ),
            marketing_policy_agreed_at=user_result.marketing_policy_agreed_at
            and user_result.marketing_policy_agreed_at.replace(
                tzinfo=timezone.utc,
            ),
            push_agreed_at=user_result.push_agreed_at
            and user_result.push_agreed_at.replace(
                tzinfo=timezone.utc,
            ),
        )

    async def get_user_by_account(self, *, account: str) -> User | None:
        stmt = select(UserTable).where(UserTable.account == account)
        return await self._get_user_table(stmt)

    async def get_user_by_user_id(self, *, user_id: int) -> User | None:
        stmt = select(UserTable).where(UserTable.id == user_id)
        return await self._get_user_table(stmt)

    async def get_user_by_phone(self, *, phone: str) -> User | None:
        stmt = select(UserTable).where(UserTable.phone == phone)
        return await self._get_user_table(stmt)

    async def save_user(self, *, user: User) -> User:
        now = datetime.now(tz=timezone.utc)
        user_row = dict(
            id=user.id,
            account=user.account,
            phone=user.phone,
            birth=user.birth,
            verified_at=user.verified_at,
            privacy_policy_agreed_at=user.privacy_policy_agreed_at,
            service_policy_agreed_at=user.service_policy_agreed_at,
            marketing_policy_agreed_at=user.marketing_policy_agreed_at,
            push_agreed_at=user.push_agreed_at,
        )
        stmt = insert(UserTable).values(
            created_at=now,
            **user_row
        ).on_duplicate_key_update(**user_row)
        result = await self.session.execute(stmt)
        user.id, *_ = result.inserted_primary_key_rows[0]
        return user

    async def save_certification(
        self,
        *,
        user_id: int,
        certification_type: CertificationType,
        certification: CertificationInfo,
    ):
        now = datetime.now(tz=timezone.utc)
        cert_row = CertificationTable(
            user_id=user_id,
            certification_type=certification_type,
            name=certification.name,
            gender=certification.gender,
            birth=certification.birth,
            unique_key=certification.unique_key,
            unique_in_site=certification.unique_in_site,
            created_at=now,
        )
        self.session.add(cert_row)

    async def save_face_verification_request(self, *, face_verification_request: FaceVerificationRequest):
        now = datetime.now(tz=timezone.utc)
        values = dict(
            user_id=face_verification_request.user_id,
            s3_key=face_verification_request.s3_key,
            status=face_verification_request.status,
            changed_at=face_verification_request.changed_at,
        )
        stmt = (
            insert(FaceVerificationRequestTable)
            .values(
                id=face_verification_request.id,
                requested_at=now,
                **values,
            )
            .on_duplicate_key_update(**values)
        )
        result = await self.session.execute(stmt)
        face_verification_request.id, *_ = result.inserted_primary_key_rows[0]

    async def get_user_last_face_verification_request(self, *, user_id: int) -> FaceVerificationRequest | None:
        stmt = (
            select(FaceVerificationRequestTable)
            .where(FaceVerificationRequestTable.user_id == user_id)
            .order_by(-FaceVerificationRequestTable.id)
            .limit(1)
        )
        data: FaceVerificationRequestTable = await self.session.scalar(stmt)
        if data is None:
            return None
        return FaceVerificationRequest(
            id=data.id,
            user_id=data.user_id,
            s3_key=data.s3_key,
            status=data.status,
            requested_at=data.requested_at,
            changed_at=data.changed_at,
        )

    async def delete_user(self, *, user: User):
        stmt = delete(UserTable).where(UserTable.id == user.id)
        await self.session.execute(stmt)
