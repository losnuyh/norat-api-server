from application.domain.school_board.error import AlreadySchoolMember, SchoolBoardNotOpen
from application.domain.school_board.model import QueueItem, School
from application.domain.school_board.use_case.port.input import SchoolBoardInfo, SchoolBoardInputPort, UserSchoolInfo
from application.domain.school_board.use_case.port.output import (
    SchoolSearchOutputPort,
    SchoolStoreOutputPort,
    UserOutputPort,
)
from application.error import NotFound, PermissionDenied


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
            if user is None:
                raise NotFound("user not found")
            member = school.register_member(user=user, grade=grade)
            await uow.save_school_member(member=member)
            await uow.commit()

    async def get_user_school(self, *, user_id: int) -> UserSchoolInfo:
        async with self.school_store_output as uow:
            school_member = await uow.get_user_school_member(user_id=user_id)
            if school_member is None:
                raise NotFound("user school not found")
            school = await self.school_search_output.get_school_by_code(school_code=school_member.school_code)
            if school is None:
                raise NotFound("school code is wrong, school not found")

        return UserSchoolInfo(
            school=school,
            grade=school_member.grade,
        )

    async def get_school_board_info(self, *, school_code: str, grade: int) -> SchoolBoardInfo:
        async with self.school_store_output as uow:
            school = await self.school_search_output.get_school_by_code(school_code=school_code)
            if school is None:
                raise NotFound("school code is wrong, school not found")
            member_count = await uow.get_school_member_count(school_code=school_code, grade=grade)
            return SchoolBoardInfo(
                school=school,
                grade=grade,
                total_member_count=member_count,
            )

    async def write_post(self, *, school_code: str, grade: int, writer_id: int, title: str, content: str) -> QueueItem:
        async with self.school_store_output as uow:
            school_member = await uow.get_user_school_member(user_id=writer_id)
            if school_member is None or not school_member.is_member(school_code=school_code, grade=grade):
                raise PermissionDenied("invalid request")

            member_count = await uow.get_school_member_count(
                school_code=school_member.school_code,
                grade=school_member.grade,
            )
            if member_count < 20:  # TODO: 한번 열리면 닫히지 않게
                raise SchoolBoardNotOpen("not open")

            school_member.set_queue_loader(loader=uow)
            await school_member.load_queue_items()
            if len(school_member.post_queue) >= 5:
                raise Exception  # TODO: ERROR CLASS
            queueing_item = school_member.write_post_and_queueing(
                title=title,
                content=content,
            )
            await uow.save_queue_item(item=queueing_item)
            await uow.commit()
        return queueing_item

    async def get_user_queue(self, *, school_code: str, grade: int, user_id: int) -> list[QueueItem]:
        async with self.school_store_output(read_only=True) as uow:
            school_member = await uow.get_user_school_member(user_id=user_id)
            if school_member is None or not school_member.is_member(school_code=school_code, grade=grade):
                raise PermissionDenied("invalid request")

            school_member.set_queue_loader(loader=uow)
            await school_member.load_queue_items()

        return school_member.post_queue
