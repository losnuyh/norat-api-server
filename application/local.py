from application.infra.fastapi import app
from application.infra.rdb import create_second_engine
from application.infra.sms.fake_sms import FakeSMSSender
from application.setup import setup_application
from .config import app_config

engine = create_second_engine(
    user_name=app_config.WRITE_DB_USER_NAME,
    password=app_config.WRITE_DB_USER_PASSWORD,
    host=app_config.WRITE_DB_HOST,
    port=app_config.DB_PORT,
    database=app_config.DATABASE_NAME,
)
readonly_engine = create_second_engine(
    user_name=app_config.READ_DB_USER_NAME,
    password=app_config.READ_DB_USER_PASSWORD,
    host=app_config.READ_DB_HOST,
    port=app_config.DB_PORT,
    database=app_config.DATABASE_NAME,
)

setup_application(
    app=app,
    db_engine=engine,
    readonly_engine=readonly_engine,
    sms_sender=FakeSMSSender(
        api_key=app_config.COOL_SMS_API_KEY,
        secret_key=app_config.COOL_SMS_SECRET_KEY,
        from_phone=app_config.COOL_SMS_SEND_PHONE_NUMBER,
    ),
)
