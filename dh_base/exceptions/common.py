"""Базовое исключение"""

__author__: str = "Старков Е.П."


from fastapi import HTTPException, status
from dh_base.logger import hawk


class BaseAppException(HTTPException):
    """Базовое исключение"""

    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str | None

    def __init__(self):
        try:
            raise RuntimeError()
        except RuntimeError:
            hawk.send(RuntimeError('Http Exception'), {'code': self.STATUS_CODE, 'detail': self.DETAIL})
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL)
