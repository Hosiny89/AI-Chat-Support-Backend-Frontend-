import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ---- إعدادات Alembic الأساسية ----
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---- اجعل Alembic يرى الـ Models/Base ----
# عدّل المسارات حسب هيكل مشروعك:
from db.database import Base  # فيه declarative_base()
import db.models  # مهم: استيراد الموديلات نفسها ليتم اكتشاف الجداول

target_metadata = Base.metadata

# ---- اجلب URL من متغير البيئة (لو مستخدم ${DATABASE_URL} في alembic.ini) ----
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,   # مهم لو غيرت أنواع الأعمدة
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,   # مهم لمقارنة الأنواع
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
