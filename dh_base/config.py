"""Модуль конфигов приложения"""
from typing import Literal, Type

from pydantic_settings import BaseSettings
from sqlalchemy import NullPool

__author__: str = 'Старков Е.П.'

T_MODE_TYPE: Type[Literal] = Literal['DEV', 'TEST', 'PROD']


class DBSettings:
    """Класс конфигов подключения к БД"""
    DEV_DB_HOST: str
    DEV_DB_NAME: str
    DEV_DB_LOGIN: str
    DEV_DB_PASSWORD: str
    DEV_DB_PORT: int

    TEST_DB_HOST: str
    TEST_DB_NAME: str
    TEST_DB_LOGIN: str
    TEST_DB_PASSWORD: str
    TEST_DB_PORT: int

    PROD_DB_HOST: str
    PROD_DB_NAME: str
    PROD_DB_LOGIN: str
    PROD_DB_PASSWORD: str
    PROD_DB_PORT: int

    def get_db_connection_url(self, mode: T_MODE_TYPE) -> str:
        """
        Получить строку подключения к БД

        :param mode: режим запуска приложения
        :return: строка подключения к БД
        """
        return f'{getattr(self, f"{mode}_DB_LOGIN")}:' \
               f'{getattr(self, f"{mode}_DB_PASSWORD")}' \
               f'@{getattr(self, f"{mode}_DB_HOST")}' \
               f':{getattr(self, f"{mode}_DB_PORT")}/{getattr(self, f"{mode}_DB_NAME")}'


class Settings(DBSettings, BaseSettings):
    """Класс конфигов"""
    class Config:
        """Конфигурация"""
        env_file: str = '.env'

    # Режим работы приложения
    MODE: T_MODE_TYPE

    @property
    def is_dev(self) -> bool:
        """Признак стенда для разработки"""
        return self.MODE == 'DEV'

    @property
    def is_test(self) -> bool:
        """Признак стенда для тестирования"""
        return self.MODE == 'TEST'

    @property
    def is_prod(self) -> bool:
        """Признак боевого стенда"""
        return self.MODE == 'PROD'

    @property
    def db_connection_url(self) -> str:
        """Строка подключения к БД с драйвером и СУБД"""
        return f'postgresql+asyncpg://{self.get_db_connection_url(self.MODE)}'

    @property
    def db_connection_url_sync(self) -> str:
        """Строка синхронного подключения к БД с драйвером и СУБД"""
        return f'postgresql+psycopg2://{self._connection_url}'

    @property
    def database_connection_extra_params(self) -> dict[str, Type[NullPool]]:
        """Дополнительные параметры подключения к БД"""
        if self.is_test:
            return {'pool': NullPool}

        return {}


base_config: Settings = Settings()