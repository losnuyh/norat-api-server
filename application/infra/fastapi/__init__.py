from fastapi import FastAPI

app = FastAPI(
    title="놀앗 API",
    description="""
    놀앗 api 서버
    """,
    version="0.1.0",
    openapi_url="/openapi.json",
)


class WithFastAPIRouter:
    def start(self):
        for item in self.__dir__():
            if not item.startswith("_") and item != "start":
                target = getattr(self, item)
                if hasattr(target, "__self__") and target.__self__ == self:
                    target()
