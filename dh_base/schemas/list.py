"""Схемы данных для списков"""

__author__: str = "Старков Е.П."


from pydantic import BaseModel


class NavigationSchema(BaseModel):
    page: int
    size: int
    has_more: bool


class ListParamsSchema(BaseModel):
    filter: dict | None
    navigation: NavigationSchema | None
