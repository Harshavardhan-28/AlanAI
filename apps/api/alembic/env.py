"""Alembic environment — async."""

import asyncio
import os
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None  # migrations are hand-written SQL via op.execute; no autogenerate


def run_migrations_online() -> None:
    url = os.environ.get("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    engine = create_async_engine(url)

    async def run() -> None:
        async with engine.connect() as connection:
            await connection.run_sync(
                lambda conn: context.configure(connection=conn, target_metadata=target_metadata)
            )
            async with connection.begin():
                await connection.run_sync(lambda conn: context.run_migrations())

    asyncio.run(run())


run_migrations_online()
