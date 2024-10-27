from fastapi import Request

from ..logger import logger, hawk


async def exceptions_handler(request: Request, call_next):
    """Обрабатывает исключения с отправкой данных в HAWK"""
    try:
        return await call_next(request)
    except Exception as ex:
        hawk.send()
        logger.error("Ошибка исполнения", extra={"exc": ex})
        raise ex
