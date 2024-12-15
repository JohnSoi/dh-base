"""Работа с подключениями к БД"""

__author__: str = "Старков Е.П."

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, DeclarativeMeta, sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .config import base_config

# Асинхронное подключение к БД
engine: AsyncEngine = create_async_engine(base_config.db_connection_url, **base_config.database_connection_extra_params)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Синхронное подключение к БД
sync_engine: Engine = create_engine(base_config.db_connection_url_sync, **base_config.database_connection_extra_params)
sync_session_maker: sessionmaker[Session] = sessionmaker(sync_engine)

# Базовая модель
Base: DeclarativeMeta = declarative_base()
