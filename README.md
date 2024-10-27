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

В файле ```.env``` должны быть следующие поля:
```dotenv
MODE=

REDIS_URL=
REDIS_PREFIX=
APP_NAME=

DEV_DB_HOST=
DEV_DB_NAME=
DEV_DB_LOGIN=
DEV_DB_PASSWORD=
DEV_DB_PORT=

TEST_DB_HOST=
TEST_DB_NAME=
TEST_DB_LOGIN=
TEST_DB_PASSWORD=
TEST_DB_PORT=

PROD_DB_HOST=
PROD_DB_NAME=
PROD_DB_LOGIN=
PROD_DB_PASSWORD=
PROD_DB_PORT=

HAWK_TOKEN=
LOG_LEVEL=
```
