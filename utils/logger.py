import logging
import os
import time
from enum import Enum
from typing import Optional, Callable, Any, Literal


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(self,
                 log_lvl: LogLevel = LogLevel.INFO,
                 log_target: Literal["console", "file", "both"] = "console") -> None:
        """Logger
        :param log_lvl: LogLevel
        :param log_target: Target for logs (store to file, display to console or both(file and console))
        """
        self._log = logging.getLogger("selenium")
        self._log.setLevel(LogLevel.INFO.value)
        self.log_file = self._create_log_file()
        self.log_target = log_target
        self._initialize_logging(log_lvl)

    def _create_log_file(self) -> str:
        current_time = time.strftime("%Y-%m-%d")
        log_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../tests/logs")
        )

        try:
            os.makedirs(
                log_directory, exist_ok=True
            )  # Create directory if it doesn't exist
        except Exception as e:
            raise RuntimeError(
                f"Failed to create log directory '{log_directory}': {e}"
            )

        return os.path.join(log_directory, f"log_{current_time}.log")

    def _initialize_logging(self, log_lvl: LogLevel) -> None:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        # Lot to file or both file and console
        if self.log_target in ("file", "both"):
            fh = logging.FileHandler(self.log_file, mode="w")
            fh.setFormatter(formatter)
            fh.setLevel(log_lvl.value)
            self._log.addHandler(fh)

        # Log to console or both file and console
        if self.log_target in ("console", "both"):
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            ch.setLevel(log_lvl.value)
            self._log.addHandler(ch)

    def get_instance(self) -> logging.Logger:
        return self._log

    def annotate(
        self, message: str, level: Literal["info", "warn", "debug", "error"]
    ) -> None:
        """Log a message at the specified level."""
        if level == "info":
            self._log.info(message)
        elif level == "warn":
            self._log.warning(message)
        elif level == "debug":
            self._log.debug(message)
        elif level == "error":
            self._log.error(message)
        else:
            raise ValueError(f"Invalid log level: {level}")


def log(
    data: Optional[str] = None,
    level: Literal["info", "warn", "debug", "error"] = "info",
) -> Callable:
    """Decorator to log the current method's execution.

    :param data: Custom log message to use if no docstring is provided.
    :param level: Level of the logs, e.g., info, warn, debug, error.
    """
    logger_instance = Logger()  # Get the singleton instance of Logger

    def decorator(func: Callable) -> Callable:
        def wrapper(self, *args, **kwargs) -> Any:
            # Get the method's docstring
            method_docs = format_method_doc_str(func.__doc__)

            if method_docs is None and data is None:
                raise ValueError(
                    f"No documentation available for :: {func.__name__}"
                )

            # Construct the parameter string for logging
            params_str = ", ".join(repr(arg) for arg in args)
            kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            all_params_str = ", ".join(filter(None, [params_str, kwargs_str]))

            logs = (
                method_docs
                + f" Method :: {func.__name__}()"
                + f" with parameters: {all_params_str}"
                if method_docs
                else data
                + f" Method :: {func.__name__}()"
                + f" with parameters: {all_params_str}"
            )

            logger_instance.annotate(logs, level)

            # Call the original method, passing *args and **kwargs
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def format_method_doc_str(doc_str: Optional[str]) -> Optional[str]:
    """Add a dot to the docs string if it doesn't exist."""
    if doc_str and not doc_str.endswith("."):
        return doc_str + "."
    return doc_str
