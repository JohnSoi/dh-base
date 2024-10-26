"""Базовые константы"""

__author__: str = 'Старков Е.П.'

from dataclasses import dataclass


@dataclass
class TimeInSeconds:
    """Время в секундах"""
    minute: int = 60
    hour: int = 60 * 60
    day: int = 24 * 60 * 60
    week: int = 7 * 24 * 60 * 60
    month: int = 30 * 7 * 24 * 60 * 60
