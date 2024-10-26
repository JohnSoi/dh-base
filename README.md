# Платформа экосистемы DH

---

## Описание 

Базовые механизмы приложений экосистемы DH

---

## Состав

* ```mixins``` - базовые миксины
  * ```ConvertToDictMixin``` - Миксин для перевода модели в словарь 
* ```repositories``` - базовые репозитории
  * ```BaseRepository``` - базовый абстрактный класс репозитория
  * ```EntityNotFount``` - исключение при отсутствии записи
* ```columns``` - базовые миксины колонок
  * ```IdColumns``` - колонки идентификатора и UUID
  * ```DateEditColumns``` - колонки дат (создание, обновления и удаления)
* ```consts``` - базовые константы
  * ```TimeInSeconds``` - константы времени
* ```exseptions``` - базовые исключения
  * ```BaseAppException``` - базовое исключения для экосистемы
* ```schemas``` - базовые схемы
  * ```SimpleOperationResult``` - схема ответа простой операции
---

## Подключение

Для подключения используется команда:
```bash
poetry add git+https://github.com/JohnSoi/dh-base.git
```

Далее необходима настроить базовый репозиторий. Для этого в корне проекта создается файл ```base_class.py``` со следующим содержимым:
```python
from dh_base.repositories import BaseRepository as PlatformBaseREpositories
from dh_autoservice.database import async_session_maker, sync_session_maker

class BaseRepository(PlatformBaseREpositories):
    @property
    def async_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return async_session_maker

    @property
    def sync_session_maker(self) -> sessionmaker[Session]:
        return sync_session_maker
```

