from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def create_second_engine(
    *,
    user_name: str,
    password: str,
    host: str,
    port: int | str,
    database: str,
) -> AsyncEngine:
    return create_async_engine(
        f"mysql+aiomysql://{user_name}:{password}@{host}:{port}/{database}",
        echo=True,
    )
