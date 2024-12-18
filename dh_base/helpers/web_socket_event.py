"""Модуль менеджера работы с сокетами"""
from typing import Dict, Any

from fastapi import WebSocket

from step_education.exceptions import NotConnectedSocket, ErrorEventName


class WebSocketConnectionManager:
    """Менеджер работы с сокетами"""
    def __init__(self) -> None:
        """Менеджер работы с сокетами"""
        self._socket: WebSocket | None = None

    async def connect(self, socket: WebSocket) -> None:
        """
        Подключение сокета

        :param socket: экземпляр сокета
        """
        self._socket = socket
        await self._socket.accept()

    async def disconnect(self) -> None:
        """Отключение от сокета"""
        if self._socket is None:
            raise NotConnectedSocket()

        await self._socket.close()

    async def publish(self, event_name: str, data: Dict[str, Any]) -> None:
        """
        Публикация события

        :param event_name: имя события вида - <область события>.<название>
        [<дополнительные данные>:<ИД пользователя публикации>]
        :param data: данные для события
        """
        self._validate_name(event_name)

        if self._socket is None:
            raise NotConnectedSocket()

        await self._socket.send_json({
            'event': event_name,
            'data': data
        }, mode='text')

    async def handle_message(self, message) -> None:
        """Обработчик сообщения"""
        print(message)

    @staticmethod
    def _validate_name(name: str) -> None:
        """
        Проверка имени события

        :param name: имя события
        """
        if '.' not in name:
            raise ErrorEventName()


manager = WebSocketConnectionManager()
