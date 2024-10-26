"""Модуль базовых колонок"""

__author__: str = 'Старков Е.П.'

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import Uuid, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class IdColumns:
    """Поля идентификаторов для моделей"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[UUID] = mapped_column(Uuid)


@dataclass
class DateEditColumns:
    """Поля для хранения дат изменения записи"""
    date_create: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    date_update: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    date_delete: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
