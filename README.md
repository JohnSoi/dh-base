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


