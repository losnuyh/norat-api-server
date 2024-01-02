from . import SMSSender


class FakeSMSSender(SMSSender):
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

    async def send_message(
        self,
        *,
        phone: str,
        message: str,
    ):
        print("=" * 20)
        print("KEY: ", self._api_key, ", SECRET: ", self._secret_key)
        print("SEND TO MESSAGE")
        print("TO: ", phone)
        print("FROM: ", self._from_phone)
        print("--- MESSAGE")
        print(message)
        print("-" * 10)
        print("=" * 20)
