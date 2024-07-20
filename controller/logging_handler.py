import datetime
import json
import logging.handlers
from logging import Logger
from typing import List

from starlette.requests import Request


class LoggingHandlerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class LoggingHandler(metaclass=LoggingHandlerMeta):
    def __init__(self):
        self.logger = None

    @staticmethod
    def _build_rq_payload(rq: Request, rq_body) -> dict:
        return {
            'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'url': rq.url.path,
            'body': json.loads(rq_body.decode())
        }

    def get_logger(self) -> Logger:
        if not self.logger:
            formatter = logging.Formatter("%(message)s")
            info_handler = logging.handlers.WatchedFileHandler("./family_tree_matcher_info.json")
            info_handler.setFormatter(formatter)
            info_handler.setLevel("INFO")

            error_handler = logging.handlers.WatchedFileHandler("./family_tree_matcher_error.json")
            error_handler.setFormatter(formatter)
            error_handler.setLevel("ERROR")

            logger = logging.getLogger()
            logger.setLevel("INFO")
            logger.addHandler(info_handler)
            logger.addHandler(error_handler)

            self.logger = logger

        return self.logger

    def log_info(self, rq: Request, rq_body):
        self.logger.info(LoggingHandler._build_rq_payload(rq, rq_body))

    def log_error(self, rq: Request, rq_body, error: List[str]):
        self.logger.error(LoggingHandler._build_rq_payload(rq, rq_body).update(
            {'error': error}
        ))
