import logging
from datetime import date

import aiohttp
from starlette import status

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
                f"https://api.iamport.kr/certifications/{imp_uid}",
                headers={
                    "Authorization": access_token,
                },
            )

            response_body = await response.json()
            if response.status != status.HTTP_200_OK:
                logging.error(response_body)
                return None

        """
        {
            'code': 0,
            'message': None,
            'response': {
                'birth': 744822000,
                'birthday': '1993-08-09',
                'carrier': 'LGT_MVNO',
                'certified': True,
                'certified_at': 1706626607,
                'foreigner': False,
                'foreigner_v2': None,
                'gender': 'female',
                'imp_uid': 'imp_128565019656',
                'merchant_uid': 'mid_1706626562947',
                'name': '임민영',
                'origin': 'data:text/html,%20%20%20%20%3Chtml%3E%0A%20%20%20%20%20%20%3Chead%3E%0A%20%20%20%20%20%20%20%20%3Cmeta%20http-equiv=%22content-type%22%20content=%22text/html;%20charset=utf-8%22%3E%0A%20%20%20%20%20%20%20%20%3Cmeta%20name=%22viewport%22%20content=%22width=device-width,%20initial-scale=1.0,%20user-scalable=no%22%3E%0A%0A%20%20%20%20%20%20%20%20%3Cscript%20type=%22text/javascript%22%20src=%22https://cdn.iamport.kr/v1/iamport.js%22%3E%3C/script%3E%0A%20%20%20%20%20%20%3C/head%3E%0A%20%20%20%20%20%20%3Cbody%3E%3C/body%3E%0A%20%20%20%20%3C/html%3E%0A%20%20', 'pg_provider': 'danal', 'pg_tid': '202401302356050668095010', 'phone': '01047374146', 'unique_in_site': 'MC0GCCqGSIb3DQIJAyEAdbCGO2F0fAgUxZk9eL2lyhSo0Il5z0yi4XdGzKevvlI=', 'unique_key': '263mu4SVXONzpqUdVIJ4SVaG+GW6GQZqGi/P9e684oQnOvnZWPb9svZYNrKZeeJeQOf+CCoEVtaIjSDK7Q5EFA==',
            }
        }
        """
        # TODO: unqiue_key, unique_in_site 처리 방법 고민, 필드 제거 ?
        data = response_body["response"]
        return CertificationInfo(
            name=data["name"],
            gender=data["gender"],
            birth=date.fromisoformat(data["birthday"]),
            unique_key="u-1234",
            unique_in_site="u-s-123",
        )
