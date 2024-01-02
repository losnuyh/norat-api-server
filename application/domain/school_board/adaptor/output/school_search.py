import json

import aiohttp

from application.domain.school_board.model import SchoolVO
from application.domain.school_board.use_case.port.output import SchoolSearchOutputPort


class SchoolSearchOutputAdaptor(SchoolSearchOutputPort):
    async def search_school_by_name(self, *, keyword: str) -> list[SchoolVO]:
        search_result: list[SchoolVO] = []
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://open.neis.go.kr/hub/schoolInfo?type=json&SCHUL_NM={keyword}",
            ) as response:
                raw = await response.text()
                result = json.loads(raw)

                if (result.get("RESULT", {}).get("MESSAGE", {})) == "해당하는 데이터가 없습니다.":
                    return search_result

                for item in result.get("schoolInfo")[1].get("row"):
                    search_result.append(
                        SchoolVO(
                            school_code=item["SD_SCHUL_CODE"],
                            name=item["SCHUL_NM"],
                            address=item["ORG_RDNMA"],
                        ),
                    )
        return search_result
