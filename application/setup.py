from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette import status

from application.config import app_config
from application.domain.authentication.adaptor.input.http import AuthenticationHttpInputAdaptor, authentication_router
from application.domain.authentication.adaptor.output.sms_sender import SMSCodeSenderOutputAdaptor
from application.domain.authentication.adaptor.output.store import AuthenticationStoreAdaptor
from application.domain.authentication.error import AuthenticationFail, PasswordNotMatched, PasswordValidationFail
from application.domain.authentication.use_case import AuthenticationUseCase
from application.domain.school_board.adaptor.input.http import SchoolBoardHttpInputAdaptor, school_board_router
from application.domain.school_board.adaptor.output import SchoolSearchOutputAdaptor
from application.domain.school_board.use_case import SchoolBoardUseCase
from application.domain.user.adaptor.input.http import UserHttpInputAdaptor, user_router
from application.domain.user.adaptor.output.store import UserStoreAdaptor
from application.domain.user.error import AccountIsDuplicated
from application.domain.user.use_case import UserUseCase
from application.infra.sms import SMSSender


def setup_exception_handlers(application: FastAPI):
    @application.exception_handler(AuthenticationFail)
    @application.exception_handler(AccountIsDuplicated)
    @application.exception_handler(PasswordNotMatched)
    @application.exception_handler(PasswordValidationFail)
    def handle_bad_request(request: Request, exc: AuthenticationFail):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
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
    )
    user_http_application = UserHttpInputAdaptor(
        input=user_use_case,
    )

    school_use_case = SchoolBoardUseCase(
        search_output=SchoolSearchOutputAdaptor(
            key=app_config.NEIS_KEY,
        ),
    )
    school_http_application = SchoolBoardHttpInputAdaptor(
        input_adaptor=school_use_case,
    )

    user_http_application.start()
    authentication_http_application.start()
    school_http_application.start()

    app.include_router(authentication_router, prefix="/authentication")
    app.include_router(user_router, prefix="/user")
    app.include_router(school_board_router, prefix="/school")

    setup_exception_handlers(app)
