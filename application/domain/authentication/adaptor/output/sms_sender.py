from application.domain.authentication.model import AuthenticationPhone
from application.domain.authentication.use_case.port.output import CodeSenderOutputPort
from application.infra.sms import SendFail, SMSSender

AUTHENTICATION_SMS_FORMAT = """[놀앗] 인증번호 [{code}] 입니다\n타인에게 노출되지 않도록 주의하세요."""


class SMSCodeSenderOutputAdaptor(CodeSenderOutputPort):
    def __init__(
        self,
        sms_sender: SMSSender,
    ):
        self.cool_sms = sms_sender

    async def send_code(self, *, authentication_phone: AuthenticationPhone) -> bool:
        try:
            await self.cool_sms.send_message(
                phone=authentication_phone.phone,
                message=AUTHENTICATION_SMS_FORMAT.format(code=authentication_phone.code),
            )
            return True
        except SendFail:
            return False
