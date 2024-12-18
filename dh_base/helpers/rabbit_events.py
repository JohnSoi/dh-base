"""Модуль для работы с RabbitMQ"""
import json
from typing import Dict, Any, Callable

from pika import BlockingConnection, ConnectionParameters  # type: ignore[import-untyped]
from pika.adapters.blocking_connection import BlockingChannel  # type: ignore[import-untyped]

from dh_base.config import base_config


class RabbitEventHelper:
    """Хелпер для работы с RabbitMQ"""
    _CONNECTION: BlockingConnection = BlockingConnection(ConnectionParameters(base_config.RABBIT_MQ_HOST))
    _CHANNEL: BlockingChannel = _CONNECTION.channel()

    def __init__(self, queue_name: str = 'main') -> None:
        """
        Хелпер для работы с брокером RabbitMQ

        :param queue_name: название очереди. По - умолчанию: main
        """
        self._queue_name: str = queue_name
        self._CHANNEL.queue_declare(self._queue_name)

    def publish(self, params: Dict[str, Any] | None = None) -> None:
        """
        Публикация события в брокер

        :param params: параметры события
        """
        body: str = ''

        if params:
            body = json.dumps(params)

        self._CHANNEL.basic_publish(
            exchange='',
            routing_key=self._queue_name,
            body=body.encode()
        )

        print(f' [x] (EventHelper.publish) Публикация в {self._queue_name}')

    def subscribe(self, callback: Callable) -> None:
        """
        Подписка на событие

        :param callback: обработчик события
        """
        self._CHANNEL.basic_consume(
            queue=self._queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
