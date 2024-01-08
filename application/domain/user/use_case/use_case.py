from datetime import date

from application.domain.authentication.model import UserData
from application.domain.user.error import AccountIsDuplicated
from application.domain.user.model import User
from application.domain.user.use_case.port.input import UserInputPort
from application.domain.user.use_case.port.output import AuthenticationOutputPort, UserStoreOutputPort


class UserUseCase(UserInputPort):
    def __init__(
        self,
        *,
        user_store: UserStoreOutputPort,
        auth_app: AuthenticationOutputPort,
    ):
        self.user_store = user_store
        self.auth_app = auth_app

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
