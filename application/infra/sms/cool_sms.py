import logging
import hashlib
import hmac
import uuid
from datetime import datetime, timezone

import aiohttp

from . import SMSSender


class CoolSMSSender(SMSSender):
    def __init__(
        self,
        *,
        api_key: str,
        secret_key: str,
        from_phone: str,
    ):
        self._api_key = api_key
        self._secret_key = secret_key
        self._from_phone = from_phone

    def _get_headers(self) -> dict[str, str]:
        date_now = datetime.now(tz=timezone.utc).isoformat()
        salt = str(uuid.uuid1().hex)
        combined_string = date_now + salt
        signature = hmac.new(
            self._secret_key.encode(),
            combined_string.encode(),
            hashlib.sha256,
        ).hexdigest()
        return {
            "Authorization": f"HMAC-SHA256 ApiKey={self._api_key}, Date={date_now}, salt={salt}, signature={signature}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def _get_body(self, to: str, message: str) -> dict:
        return {
            "message": {
                "to": to,
                "from": self._from_phone,
                "text": message,
            },
        }

    async def send_message(
        self,
        phone: str,
        message: str,
    ):
        async with aiohttp.ClientSession(
            headers=self._get_headers(),
        ) as session:
            async with session.post(
                "https://api.coolsms.co.kr/messages/v4/send",
                json=self._get_body(phone, message),
            ) as response:
                if response.status >= 400:
                    json_body = await response.json()
                    logging.warning(json_body)
