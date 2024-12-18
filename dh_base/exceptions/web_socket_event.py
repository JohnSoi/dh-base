"""Модуль исключений при работе с веб сокетом"""
from dh_base.exceptions.common import BaseAppException


class NotConnectedSocket(BaseAppException):
    """Нет подключения к сокету"""
    _DETAIL = 'Не создано подключение к сокету'


class ErrorEventName(BaseAppException):
    """Некорректное имя события"""
    _DETAIL = 'Имя события должно быть вида <область события>.<название>'
