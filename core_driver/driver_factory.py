from core_driver.driver import ChromeRemoteDriver, FirefoxDriver, LocalDriver
from utils.error_handler import ErrorHandler, ErrorType
from utils.logger import Logger, LogLevel

log = Logger(log_lvl=LogLevel.INFO).get_instance()


class WebDriverFactory:
    DRIVER_MAPPING = {
        "chrome": ChromeRemoteDriver,
        "firefox": FirefoxDriver,
        "local": LocalDriver,
    }

    @staticmethod
    def create_driver(environment=None, driver_type="local"):
        log.info(f"Creating driver of type: {driver_type}")
        driver_type = driver_type.lower()
        if driver_type in WebDriverFactory.DRIVER_MAPPING:
            driver_class = WebDriverFactory.DRIVER_MAPPING[driver_type]
            return driver_class().create_driver(
                environment, driver_type
            )  # No .value needed
        else:
            raise ErrorHandler.raise_error(
                ErrorType.ENV_ERROR, environment, driver_type
            )
