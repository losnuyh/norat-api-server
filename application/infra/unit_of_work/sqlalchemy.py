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
        self.__read_only = False

    async def __aenter__(self) -> Self:
        if self.__read_only:
            session = AsyncSession(self.readonly_engine)
        else:
            session = AsyncSession(self.engine)
        self.__context_session.set(session)
        return self

    def __call__(self, read_only=False):
        self.__read_only = read_only
        return self

    @property
    def session(self):
        return self.__context_session.get("session")

    def __remove_session(self):
        self.__context_session.get("session")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        return

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
