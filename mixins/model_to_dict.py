# pylint: disable=too-few-public-methods
"""Миксин конвертации модели в словарь"""

__author__: str = 'Старков Е.П.'

from typing import Any


class ConvertToDictMixin:
    """Миксин конвертации модели в словарь. Исключает служебные поля"""
    def to_dict(self) -> dict[str, Any]:
        """Преобразовать в словарь"""
        result = {}

        for key in self.__dict__:
            if not key.startswith('_') and hasattr(self, key):
                result[key] = getattr(self, key)

        return result
