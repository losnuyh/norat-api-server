from contextvars import ContextVar
from typing import Self

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class UnitOfWork:
    engine: AsyncEngine
    readonly_engine: AsyncEngine
    __context_session: ContextVar[AsyncSession]

    def __init__(self, *, engine: AsyncEngine, readonly_engine: AsyncEngine):
        self.engine = engine
        self.readonly_engine = readonly_engine
        self.__context_session = ContextVar("session")
        self.__context_read_only = ContextVar("read_only", default=False)

    async def __aenter__(self) -> Self:
        read_only = self.__context_read_only.get()
        if read_only:
            session = AsyncSession(self.readonly_engine)
        else:
            session = AsyncSession(self.engine)
        self.__context_session.set(session)
        return self

    def __call__(self, read_only=False):
        self.__context_read_only.set(read_only)
        return self

    @property
    def session(self):
        return self.__context_session.get()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.__context_read_only.set(False)
        return

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
