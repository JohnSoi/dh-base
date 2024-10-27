import time

from fastapi import Request

from ..logger import logger


async def add_process_time_header(request: Request, call_next):
    """Добавляет время обработки в заголовок"""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Время выполнения", extra={"process_time": round(process_time, 2)})
    return response
