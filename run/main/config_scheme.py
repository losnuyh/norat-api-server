from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationConfigScheme:
    WRITE_DB_USER_NAME: str
    WRITE_DB_USER_PASSWORD: str
    WRITE_DB_HOST: str

    READ_DB_USER_NAME: str
    READ_DB_USER_PASSWORD: str
    READ_DB_HOST: str

    DB_PORT: str
    DATABASE_NAME: str

    COOL_SMS_SECRET_KEY: str
    COOL_SMS_API_KEY: str
    COOL_SMS_SEND_PHONE_NUMBER: str

    NEIS_KEY: str

    PORT_ONE_KEY: str
    PORT_ONE_SECRET: str

    USER_UPLOAD_S3_BUCKET_NAME: str
