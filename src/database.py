from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import db_settings


engine = create_async_engine(
    f'postgresql+asyncpg://{db_settings.user}:{db_settings.password}@{db_settings.host}/{db_settings.name}',
    pool_size=10,
    max_overflow=15,
)
session_factory = async_sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session
