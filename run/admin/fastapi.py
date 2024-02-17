from fastapi import FastAPI

app = FastAPI(
    title="놀앗 ADMIN API",
    description="""
    놀앗 api 서버
    """,
    version="0.1.0",
    root_path="/dev/",  # TODO: 로컬에서는 설정되지 않아야 fastapi docs가 로컬에서 보입니다.
    openapi_url="/openapi.json",
)
