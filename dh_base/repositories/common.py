# pylint: disable=unnecessary-pass
"""Модуль базового репозитория"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List
from uuid import uuid4

from sqlalchemy import Select, select, Delete, delete, Update, Insert
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeMeta, Session

from .exceptions import EntityNotFount


class BaseRepository(ABC):
    """Базовый репозиторий"""
    _DESC: bool = True
    _SEARCH_FIELD: str | None = None

    @property
    @abstractmethod
    def async_session_maker(self) -> async_sessionmaker[AsyncSession]:
        """Для работы асинхронных сессий"""

    @property
    @abstractmethod
    def sync_session_maker(self) -> sessionmaker[Session]:
        """Для работы синхронных сессий"""

    @property
    @abstractmethod
    def model(self) -> Any:
        """Получение модели"""

    @property
    @abstractmethod
    def ordering_field_name(self) -> str:
        """Поле для сортировки"""

    async def get(self, entity_id: int) -> DeclarativeMeta | None:
        """
        Получение записи по идентификатору

        :param entity_id: идентификатор записи
        :return: запись или None
        """
        async with self.async_session_maker() as async_session:
            query: Select = select(self.model).where(self.model.id == entity_id)
            result = await async_session.execute(query)

            entity: DeclarativeMeta | None = result.scalar()

            if entity:
                self._after_read(entity)

        return entity

    async def get_with_check(self, entity_id: int) -> DeclarativeMeta:
        """
        Получение записи по идентификатору с проверкой существования

        :param entity_id: идентификатор записи
        :return: запись
        """
        entity: DeclarativeMeta | None = await self.get(entity_id)

        if not entity:
            raise EntityNotFount()

        return entity

    def sync_create(self, payload):
        with self.sync_session_maker() as async_session:
            with async_session.begin():
                new_entity: DeclarativeMeta = self.model()

                for key in payload:
                    if hasattr(new_entity, key):
                        setattr(new_entity, key, payload[key])

                self._fill_main_fields(new_entity)
                self._before_create(new_entity)
                async_session.add(new_entity)

            async_session.commit()
            self._after_create(new_entity)

            return new_entity

    async def create(self, payload: Dict[str, Any]) -> DeclarativeMeta:
        """Создание записи по данным"""
        try:
            async with self.async_session_maker() as async_session:
                async with async_session.begin():
                    new_entity: DeclarativeMeta = self.model()

                    for key in payload:
                        if hasattr(new_entity, key):
                            setattr(new_entity, key, payload[key])

                    self._fill_main_fields(new_entity)
                    self._before_create(new_entity)
                    async_session.add(new_entity)

                await async_session.commit()
                self._after_create(new_entity)

                return new_entity
        except InvalidRequestError:
            await async_session.rollback()
            raise

    async def list(
            self,
            filters: Dict[str, Any],
            navigation: Dict[str, int | bool] | None = None
    ) -> List[DeclarativeMeta]:
        """
        Список сущностей с применением фильтрации и навигации

        :param filters: фильтра
        :param navigation: навигация
        :return: список записей
        """
        query: Select = select(self.model)

        if navigation:
            page_size: int = navigation.get('pageSize', 0)
            offset: int = navigation.get('page', 0) * page_size
            query = query.limit(page_size).offset(offset)

        if filters and filters.get('search_str') and self._SEARCH_FIELD:
            query = query.where(
                getattr(self.model, self._SEARCH_FIELD).ilike(f'%{filters.get("search_str")}%')
            )

        query = self._before_list(query, filters)

        sort_field = getattr(self.model, self.ordering_field_name)
        query = query.order_by(sort_field.desc() if self._DESC else sort_field.asc())
        async with self.async_session_maker() as async_session:
            temp_result = await async_session.execute(query)

            if not temp_result:
                return []

            result = list(temp_result.scalars().all())
            self._after_list(result, filters, navigation)

        return result

    async def update(self, entity_id: int, new_entity_data: Dict[str, Any]) -> DeclarativeMeta:
        """
        Обновление записи

        :param entity_id: идентификатор записи
        :param new_entity_data: новые данные для записи
        :return: обновленная запись
        """
        entity: DeclarativeMeta = await self.get_with_check(entity_id)

        await self._before_update(entity, new_entity_data)

        for key in new_entity_data:
            if hasattr(entity, key):
                setattr(entity, key, new_entity_data[key])

        if hasattr(entity, 'date_update'):
            entity.date_update = datetime.now()

        try:
            async with self.async_session_maker() as async_session:
                async with async_session.begin():
                    async_session.add(entity)

                await async_session.commit()
                self._after_update(entity)

                return entity
        except InvalidRequestError:
            await async_session.rollback()
            raise

    async def delete(self, entity_id: int) -> None:
        """
        Удаление записи. Сначала запись помечается на удаление, а после удаляется.
        Срок удаления управляется параметром DELETE_ITEM_AFTER_DAYS

        :param entity_id: идентификатор записи
        """
        entity: DeclarativeMeta = await self.get_with_check(entity_id)
        self._before_delete(entity)

        async with self.async_session_maker() as async_session:
            if hasattr(entity, 'date_delete'):
                if entity.date_delete:
                    query: Delete = delete(self.model).where(self.model.id == entity_id)
                    await async_session.execute(query)
                else:
                    await self.update(entity_id, {
                        'date_delete': datetime.now(), 'is_active': False
                    })
            else:
                query: Delete = delete(self.model).where(self.model.id == entity_id)
                await async_session.execute(query)

        self._after_delete(entity)

    async def manual_execute(self, query: Update | Select | Delete | Insert) -> Any:
        """
        Ручное выполнение запроса

        @param query: запрос
        @return: результат
        """
        async with self.async_session_maker() as async_session:
            await async_session.execute(query)

    async def find_one_or_none(self, **filter_by):
        """
        Найти одну запись или None

        @param filter_by: фильтры
        @return: модель или None
        """
        async with self.async_session_maker() as async_session:
            query = select(self.model).filter_by(**filter_by)
            result = await async_session.execute(query)

            return result.unique().scalar_one_or_none()

    @staticmethod
    def _before_create(new_entity: DeclarativeMeta) -> None:
        """
        Обработка перед сохранением

        :param new_entity: новая запись
        """
        pass

    @staticmethod
    def _after_create(new_entity: DeclarativeMeta) -> None:
        """
        Обработка после сохранением

        :param new_entity: новая запись
        """
        pass

    @staticmethod
    def _before_list(query: Select, _: Dict[str, Any]) -> Select:
        """
        Применение фильтров

        :param query: запрос
        :param _: фильтра
        :return: экземпляр запроса с фильтрами
        """
        return query

    @staticmethod
    def _after_list(
            result: List[DeclarativeMeta],
            filters: Dict[str, Any],
            navigation: Dict[str, int] | None
    ) -> None:
        """
        Обработка результата списка

        :param result: список записей
        :param filters: фильтры
        :param navigation: навигация
        """
        pass

    @staticmethod
    async def _before_update(entity: DeclarativeMeta, new_entity_data: Dict[str, Any]) -> None:
        """
        Обработчик перед сохранением

        :param entity: запись
        :param new_entity_data: новые данные записи
        """
        pass

    @staticmethod
    def _after_update(entity: DeclarativeMeta) -> None:
        """
        Обработчик после обновления

        :param entity: запись
        """
        pass

    @staticmethod
    def _before_delete(entity: DeclarativeMeta) -> None:
        """
        Обработчик перед удалением

        :param entity: запись
        """
        pass

    @staticmethod
    def _after_delete(entity: DeclarativeMeta) -> None:
        """
        Обработчик после удалением

        :param entity: запись
        """
        pass

    @staticmethod
    def _after_read(entity: DeclarativeMeta) -> None:
        """
        Обработчик после чтения записи

        :param entity: запись
        """

    @staticmethod
    def _fill_main_fields(new_entity: DeclarativeMeta) -> None:
        """Заполнение стандартных полей при наличии"""
        if hasattr(new_entity, 'id'):
            new_entity.id = None
        if hasattr(new_entity, 'date_create'):
            new_entity.date_create = datetime.now()
        if hasattr(new_entity, 'date_update'):
            new_entity.date_update = datetime.now()
        if hasattr(new_entity, 'date_delete'):
            new_entity.date_delete = None
        if hasattr(new_entity, 'uuid'):
            new_entity.uuid = uuid4()
        if hasattr(new_entity, 'is_active'):
            new_entity.is_active = True
