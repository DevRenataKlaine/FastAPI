from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

from fast_zero.settings import Settings

Base = declarative_base()
engine = create_async_engine(Settings().DATABASE_URL)  # type: ignore


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
