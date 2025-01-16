import logging
import os
import time
from enum import Enum
from typing import Optional, Callable, Any, Literal
from threading import Lock


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR


class Singleton(type):
    _instances = {}
    _lock = Lock()  # Ensure thread safety

    def __call__(cls, *args, **kwargs) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(
        self,
        log_lvl: LogLevel = LogLevel.INFO,
        log_target: Literal["console", "file", "both"] = "console",
    ) -> None:
        self._log = logging.getLogger("selenium")
        self._log.setLevel(log_lvl.value)
        self.log_file = self._create_log_file()
        self.log_target = log_target
        self._initialize_logging(log_lvl)

    def _create_log_file(self) -> str:
        current_time = time.strftime("%Y-%m-%d")
        log_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../tests/logs")
        )

        try:
            os.makedirs(log_directory, exist_ok=True)
        except Exception as e:
            raise RuntimeError(
                f"Failed to create log directory '{log_directory}': {e}"
            )

        return os.path.join(log_directory, f"log_{current_time}.log")

    def _initialize_logging(self, log_lvl: LogLevel) -> None:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        if self.log_target in ("file", "both"):
            fh = logging.FileHandler(self.log_file, mode="a")
            fh.setFormatter(formatter)
            fh.setLevel(log_lvl.value)
            self._log.addHandler(fh)

        if self.log_target in ("console", "both"):
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            ch.setLevel(log_lvl.value)
            self._log.addHandler(ch)

    def get_instance(self) -> logging.Logger:
        return self._log

    def annotate(self, message: str, level: LogLevel) -> None:
        if level == LogLevel.INFO:
            self._log.info(message)
        elif level == LogLevel.WARNING:
            self._log.warning(message)
        elif level == LogLevel.DEBUG:
            self._log.debug(message)
        elif level == LogLevel.ERROR:
            self._log.error(message)
        else:
            raise ValueError(f"Invalid log level: {level}")


def log(data: Optional[str] = None, level: LogLevel = LogLevel.INFO) -> Callable:
    logger_instance = Logger()  # Get the singleton instance of Logger

    def decorator(func: Callable) -> Callable:
        def wrapper(self, *args, **kwargs) -> Any:
            method_docs = format_method_doc_str(func.__doc__)
            log_message = (
                (method_docs or data or "")
                + f" Method :: {func.__name__}() with parameters: {', '.join(map(str, args))}"
            )
            logger_instance.annotate(log_message, level)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def format_method_doc_str(doc_str: Optional[str]) -> Optional[str]:
    if doc_str and not doc_str.endswith("."):
        return doc_str + "."
    return doc_str
