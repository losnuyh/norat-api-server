from datetime import date

from application.domain.authentication.model import UserData
from application.domain.user.error import AccountIsDuplicated, CertificationIsWrong
from application.domain.user.model import User
from application.domain.user.use_case.port.input import UserInputPort
from application.domain.user.use_case.port.output import (
    AuthenticationOutputPort,
    CertificationOutputPort,
    UserStoreOutputPort,
)
from application.error import InvalidData, NotFound


class UserUseCase(UserInputPort):
    def __init__(
        self,
        *,
        user_store: UserStoreOutputPort,
        auth_app: AuthenticationOutputPort,
        certification_app: CertificationOutputPort,
    ):
        self.user_store = user_store
        self.auth_app = auth_app
        self.cert_app = certification_app

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
        async with self.user_store as uow:
            user = await uow.get_user_by_account(account=account)
            return user is not None

    async def self_certification(self, *, user_id: int, imp_uid: str):
        """
        1. imp_uid로 유저 정보 받아 오는 outputProt 메소드 호출
        2. user_id로 받아온 user 정보와 비교
        * user 정보가 만 14세가 넘어야 함
        3. 같으면 성공 다르면 실패
        """

        async with self.user_store(read_only=True) as uow:
            user = await uow.get_user_by_user_id(user_id=user_id)
            if user.get_current_age() < 14:
                raise InvalidData(f"wrong user age: {user.get_current_age()=}")
            if user is None:
                raise NotFound(f"user not exist, {user_id=}")

            certification_info = await self.cert_app.get_certification_info(imp_uid=imp_uid)
            if certification_info is None:
                raise CertificationIsWrong(f"wrong imp_uid, {imp_uid=}")
            ...

            if user.birth != certification_info.birth:
                raise CertificationIsWrong(f"not matched, {user.birth=}, {certification_info.birth=}")
