import asyncio
import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from core import engine

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from core.config import settings  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

from models import BaseUUIDModel  # noqa

target_metadata = BaseUUIDModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_online():
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        connectable = engine

    if isinstance(connectable, AsyncEngine):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None

        if loop and loop.is_running():
            task = loop.create_task(run_async_migrations(connectable))
            task.add_done_callback(
                lambda t: print(
                    f"Task done with result={t.result()}  << return val of main()"
                )
            )
        else:
            asyncio.run(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable.connect())


# Then use their setup for async connection/running of the migration
async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


# But the outer layer still allows sychronous execution also.
run_migrations_online()
