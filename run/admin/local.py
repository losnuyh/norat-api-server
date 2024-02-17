from application.infra.rdb import create_second_engine
from application.infra.sms.fake_sms import FakeSMSSender
from common.config import app_config as common_config

from .fastapi import app
from .setup import setup_application

engine = create_second_engine(
    user_name=common_config.WRITE_DB_USER_NAME,
    password=common_config.WRITE_DB_USER_PASSWORD,
    host=common_config.WRITE_DB_HOST,
    port=common_config.DB_PORT,
    database=common_config.DATABASE_NAME,
)
readonly_engine = create_second_engine(
    user_name=common_config.READ_DB_USER_NAME,
    password=common_config.READ_DB_USER_PASSWORD,
    host=common_config.READ_DB_HOST,
    port=common_config.DB_PORT,
    database=common_config.DATABASE_NAME,
)

setup_application(
    app=app,
    db_engine=engine,
    readonly_engine=readonly_engine,
    sms_sender=FakeSMSSender(
        api_key=common_config.COOL_SMS_API_KEY,
        secret_key=common_config.COOL_SMS_SECRET_KEY,
        from_phone=common_config.COOL_SMS_SEND_PHONE_NUMBER,
    ),
)
