from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
from dotenv import load_dotenv
from main.database import metadata

# Load .env
load_dotenv()

# SQLite URL
DATABASE_URL = "sqlite:///sqlite.db"

# Alembic config
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
