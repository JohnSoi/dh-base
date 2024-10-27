import logging
from datetime import datetime, UTC
from typing import Dict, Any

from pythonjsonlogger import jsonlogger

from dh_base.config import base_config
from hawkcatcher import Hawk

hawk = Hawk(base_config.HAWK_TOKEN)


logger: logging.Logger = logging.getLogger()
log_handler: logging.StreamHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)

        if not log_record.get('timestamp'):
            now: str = datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


formatter: CustomJsonFormatter = CustomJsonFormatter('%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.setLevel(base_config.LOG_LEVEL)
