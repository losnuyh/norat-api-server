from datetime import date

import aiohttp

from application.domain.user.model import CertificationInfo
from application.domain.user.use_case.port.output import CertificationOutputPort


class CertificationOutputAdaptor(CertificationOutputPort):
    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    async def get_certification_info(self, *, imp_uid: str) -> CertificationInfo | None:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                "https://api.iamport.kr/users/getToken",
                json={
                    "imp_key": self.key,
                    "imp_secret": self.secret,
                },
                headers={
                    "Content-Type": "application/json",
                },
            )
            response_body = await response.json()
            access_token = response_body["response"]["access_token"]

            response = await session.get(
                f"https://api.iamport.kr/certifications/${imp_uid}",
                headers={
                    "Authorization": access_token,
                },
            )

            response_body = await response.json()
            print("status >>>>>>", response.status)
            print("body >>>>>>", response_body)
        return CertificationInfo(
            name="soul",
            gender="m",
            birth=date(year=2000, month=1, day=1),
            unique_key="u-1234",
            unique_in_site="u-s-123",
        )
