"""Базовые исключение"""

__author__: str = "Старков Е.П."


from fastapi import status

from ..exceptions import BaseAppException


class EntityNotFount(BaseAppException):
    """Не найдена запись"""

    STATUS_CODE: int = status.HTTP_409_CONFLICT
    DETAIL: str | None = "Не найдена запись по переданным параметрам"
