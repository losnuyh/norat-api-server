import json

import aiohttp

from application.domain.school_board.model import School
from application.domain.school_board.use_case.port.output import SchoolSearchOutputPort


class SchoolSearchOutputAdaptor(SchoolSearchOutputPort):
    def __init__(self, key: str):
        self.key = key

    async def search_school_by_name(self, *, keyword: str) -> list[School]:
        search_result: list[School] = []
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://open.neis.go.kr/hub/schoolInfo?type=json&SCHUL_NM={keyword}&KEY={self.key}",
            ) as response:
                raw = await response.text()
                result = json.loads(raw)

                if (result.get("RESULT", {}).get("MESSAGE", {})) == "해당하는 데이터가 없습니다.":
                    return search_result

                for item in result.get("schoolInfo")[1].get("row"):
                    search_result.append(
                        School(
                            school_code=item["SD_SCHUL_CODE"],
                            name=item["SCHUL_NM"],
                            address=item["ORG_RDNMA"],
                        ),
                    )
        return search_result

    async def get_school_by_code(self, *, school_code: str) -> School | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://open.neis.go.kr/hub/schoolInfo?type=json&SD_SCHUL_CODE={school_code}&KEY={self.key}",
            ) as response:
                if response.status != 200:
                    # TODO: logging
                    return None
                raw = await response.text()
                result = json.loads(raw)

                if (result.get("RESULT", {}).get("MESSAGE", {})) == "해당하는 데이터가 없습니다.":
                    return None

                if (
                    result.get("schoolInfo")[1].get("row") is not None
                    and len(result.get("schoolInfo")[1].get("row")) == 1
                ):
                    item = result.get("schoolInfo")[1].get("row")[0]
                    return School(
                        school_code=item["SD_SCHUL_CODE"],
                        name=item["SCHUL_NM"],
                        address=item["ORG_RDNMA"],
                    )
                return None
