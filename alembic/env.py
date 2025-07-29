from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

from fast_zero.database import Base
from fast_zero.settings import Settings     # Para pegar a URL do banco

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = Settings().DATABASE_URL  # type: ignore
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    url = Settings().DATABASE_URL  # type: ignore
    connectable: AsyncEngine = create_async_engine(
        url, poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn, target_metadata=target_metadata
            )
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
