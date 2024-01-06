from datetime import date

from application.domain.user.error import AccountIsDuplicated
from application.domain.user.model import User
from application.domain.user.use_case.port.input import UserInputPort
from application.domain.user.use_case.port.output import UserStoreOutputPort


class UserUseCase(UserInputPort):
    def __init__(self, *, user_store: UserStoreOutputPort):
        self.user_store = user_store

    async def create_user(self, *, account: str, birth: date) -> User:
        async with self.user_store as uow:
            if await uow.get_user_by_account(account=account):
                raise AccountIsDuplicated(f"account: {account} is duplicated")
            user = User(account=account, birth=birth)
            await uow.save_user(user=user)
            await uow.commit()
            return user

    async def check_account(self, *, account: str) -> bool:
        async with self.user_store as uow:
            user = await uow.get_user_by_account(account=account)
            return user is not None
