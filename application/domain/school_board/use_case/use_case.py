from application.domain.school_board.error import AlreadySchoolMember
from application.domain.school_board.model import School
from application.domain.school_board.use_case.port.input import SchoolBoardInputPort
from application.domain.school_board.use_case.port.output import (
    SchoolSearchOutputPort,
    SchoolStoreOutputPort,
    UserOutputPort,
)
from application.error import NotFound


class SchoolBoardUseCase(SchoolBoardInputPort):
    def __init__(
        self,
        *,
        search_output: SchoolSearchOutputPort,
        store_output: SchoolStoreOutputPort,
        user_output: UserOutputPort,
    ):
        self.school_search_output = search_output
        self.school_store_output = store_output
        self.user_output = user_output

    async def search_school(self, *, keyword: str) -> list[School]:
        search_list = await self.school_search_output.search_school_by_name(keyword=keyword)
        if not search_list:
            return []
        return search_list[:5]

    async def register_school_member(self, *, school_code: str, user_id: int, grade: int):
        async with self.school_store_output as uow:
            school_member = await uow.get_user_school_member(user_id=user_id)
            if school_member is not None:
                raise AlreadySchoolMember("user is already registered as school member")
            school = await self.school_search_output.get_school_by_code(school_code=school_code)
            if school is None:
                raise NotFound("school code is wrong, school not found")
            user = await self.user_output.get_user_by_user_id(user_id=user_id)
            member = school.register_member(user=user, grade=grade)
            await uow.save_school_member(member=member)
            await uow.commit()

    async def get_user_school(self, *, user_id: int) -> School:
        return School(school_code="abc", name="name", address="address")
