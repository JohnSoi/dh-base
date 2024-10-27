"""Базовые схемы данных"""

__author__: str = "Старков Е.П."

from pydantic import BaseModel


class SimpleOperationResult(BaseModel):
    """Результат операции"""

    success: bool
