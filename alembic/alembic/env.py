from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
from dotenv import load_dotenv
from main.database import metadata  # Shu yerda metadata import qilinyapti
from main.models import Base

# .env faylni yuklash (agar kerak bo‘lsa)
load_dotenv()

# Alembic konfiguratsiya fayli
config = context.config

# SQLite URL — .env dan olish yoki to‘g‘ridan-to‘g‘ri yozish
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sqlite.db")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging konfiguratsiyasi
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Shu yerda SQLAlchemy Core uchun metadata ni belgilaymiz
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline rejimda migratsiya yuritish."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online rejimda migratsiya yuritish."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
