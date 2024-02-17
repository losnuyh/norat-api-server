import boto3
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette import status

from application.domain.admin.adpator.input.http import AdminHttpInputAdaptor, admin_router
from application.domain.admin.use_case.use_case import AdminUseCase
from application.domain.authentication.adaptor.output.sms_sender import SMSCodeSenderOutputAdaptor
from application.domain.authentication.adaptor.output.store import AuthenticationStoreAdaptor
from application.domain.authentication.error import AuthenticationFail, PasswordNotMatched, PasswordValidationFail
from application.domain.authentication.use_case import AuthenticationUseCase
from application.domain.school_board.adaptor.output import SchoolSearchOutputAdaptor
from application.domain.school_board.adaptor.output.store import SchoolStoreOutputAdaptor
from application.domain.school_board.error import AlreadySchoolMember, SchoolBoardNotOpen, TooManyPostIntQueue
from application.domain.school_board.use_case import SchoolBoardUseCase
from application.domain.user.adaptor.output.certification import CertificationOutputAdaptor
from application.domain.user.adaptor.output.s3 import UserS3OutputAdaptor
from application.domain.user.adaptor.output.store import UserStoreAdaptor
from application.domain.user.error import (
    AccountIsDuplicated,
    AlreadyFaceVerified,
    CertificationIsWrong,
    FaceVerificationFail,
)
from application.domain.user.use_case import UserUseCase
from application.error import InvalidData, NotFound, PermissionDenied, ServerError
from application.infra.sms import SMSSender
from run.main.config import app_config
from run.main.http.authentication import AuthenticationHttpInputAdaptor, authentication_router
from run.main.http.school_board import SchoolBoardHttpInputAdaptor, school_board_router, user_router_in_school_board
from run.main.http.user import UserHttpInputAdaptor, user_router


def setup_exception_handlers(application: FastAPI):
    @application.exception_handler(PermissionDenied)
    @application.exception_handler(AuthenticationFail)
    @application.exception_handler(AccountIsDuplicated)
    @application.exception_handler(PasswordValidationFail)
    @application.exception_handler(CertificationIsWrong)
    @application.exception_handler(InvalidData)
    @application.exception_handler(AlreadyFaceVerified)
    @application.exception_handler(FaceVerificationFail)
    @application.exception_handler(AlreadySchoolMember)
    @application.exception_handler(SchoolBoardNotOpen)
    @application.exception_handler(TooManyPostIntQueue)
    def handle_bad_request(request: Request, exc: AuthenticationFail):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(exc)},
        )

    @application.exception_handler(NotFound)
    @application.exception_handler(PasswordNotMatched)
    def handle_not_found_request(request: Request, exc: AuthenticationFail):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": str(exc)},
        )

    @application.exception_handler(InvalidTokenError)
    @application.exception_handler(ExpiredSignatureError)
    def handler_token_error(request: Request, exc):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": "Not authenticated",
            },
            headers={"WWW-Authenticated": "Bearer"},
        )

    @application.exception_handler(ServerError)
    def handler_server_error(request: Request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(exc)},
        )


def setup_application(
    *,
    app: FastAPI,
    db_engine: AsyncEngine,
    readonly_engine: AsyncEngine,
    sms_sender: SMSSender,
):
    authentication_use_case = AuthenticationUseCase(
        code_sender=SMSCodeSenderOutputAdaptor(sms_sender=sms_sender),
        auth_store=AuthenticationStoreAdaptor(
            engine=db_engine,
            readonly_engine=readonly_engine,
        ),
    )
    authentication_http_application = AuthenticationHttpInputAdaptor(
        input_adaptor=authentication_use_case,
    )
    user_use_case = UserUseCase(
        user_store=UserStoreAdaptor(
            engine=db_engine,
            readonly_engine=readonly_engine,
        ),
        auth_app=authentication_use_case,
        certification_app=CertificationOutputAdaptor(
            key=app_config.PORT_ONE_KEY,
            secret=app_config.PORT_ONE_SECRET,
        ),
        s3_app=UserS3OutputAdaptor(
            s3_client=boto3.client("s3"),
            bucket_name=app_config.USER_UPLOAD_S3_BUCKET_NAME,
        ),
    )
    user_http_application = UserHttpInputAdaptor(
        input=user_use_case,
    )

    school_use_case = SchoolBoardUseCase(
        search_output=SchoolSearchOutputAdaptor(
            key=app_config.NEIS_KEY,
        ),
        store_output=SchoolStoreOutputAdaptor(
            engine=db_engine,
            readonly_engine=readonly_engine,
        ),
        user_output=user_use_case,
    )
    school_http_application = SchoolBoardHttpInputAdaptor(
        input_adaptor=school_use_case,
    )

    admin_use_case = AdminUseCase(
        user_output=user_use_case,
    )
    admin_http_application = AdminHttpInputAdaptor(
        input=admin_use_case,
    )

    user_http_application.start()
    authentication_http_application.start()
    school_http_application.start()
    admin_http_application.start()

    app.include_router(authentication_router, prefix="/authentication")
    app.include_router(user_router, prefix="/user")
    app.include_router(user_router_in_school_board, prefix="/user")
    app.include_router(school_board_router, prefix="/school")
    app.include_router(admin_router, prefix="/admin")

    setup_exception_handlers(app)
