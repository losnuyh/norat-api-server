from fastapi import FastAPI

app = FastAPI(
    title="놀앗 API",
    description="""
    놀앗 api 서버
    """,
    version="0.1.0",
    openapi_url="/openapi.json",
)
