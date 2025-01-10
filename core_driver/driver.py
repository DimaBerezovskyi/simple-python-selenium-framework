import os
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.remote_connection import RemoteConnection
from webdriver_manager.chrome import ChromeDriverManager
from core_driver.driver_options import _init_driver_options
from utils.error_handler import ErrorHandler, ErrorType
from utils.logger import Logger, LogLevel
from properties import Properties
from utils.yaml_reader import YAMLReader

log = Logger(log_lvl=LogLevel.INFO).get_instance()


def _get_driver_path(driver_type=None):
    if driver_type is None:
        ErrorHandler.raise_error(ErrorType.UNSUPPORTED_DRIVER_TYPE)

    project_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    driver_path = os.path.join(project_dir, "resources", driver_type)

    if not os.path.exists(driver_path):
        ErrorHandler.raise_error(ErrorType.DRIVER_NOT_FOUND, driver_type)

    return driver_path


def _configure_driver(driver, environment):
    driver.maximize_window()
    driver.implicitly_wait(3)
    driver.get(Properties.get_base_url(environment))
    log.info(
        f"Configure driver and base url: {Properties.get_base_url(environment)}"
    )


class Driver(ABC):
    @abstractmethod
    def create_driver(self, environment, dr_type):
        pass

    def get_desired_caps(self, browser="chrome"):
        caps = YAMLReader.read_caps(browser)
        log.info(f"Capabilities for driver {caps}")
        return caps


class LocalDriver(Driver):
    def create_driver(self, environment=None, dr_type="local"):
        """Tries to use ChromeDriverManager to install the latest driver,
        and if it fails, it falls back to a locally stored driver in resources."""
        driver = None
        try:
            driver_path = ChromeDriverManager().install()
            options = _init_driver_options(dr_type=dr_type)
            driver = webdriver.Chrome(
                service=ChromeService(executable_path=driver_path), options=options
            )
            log.info(
                f"Created local Chrome driver with session: {driver.session_id}"
            )
        except Exception as e:
            log.error(f"Failed to create Chrome driver  {e}")
            driver = webdriver.Chrome(
                service=ChromeService(_get_driver_path(dr_type)),
                options=_init_driver_options(dr_type=dr_type),
            )
        _configure_driver(driver, environment)
        return driver


class ChromeRemoteDriver(Driver):
    def create_driver(self, environment=None, dr_type=None):
        caps = self.get_desired_caps()
        driver = webdriver.Remote(
            command_executor=RemoteConnection("your remote URL"),
            desired_capabilities={"LT:Options": caps},  # noqa
        )
        log.info(f"Remote Chrome driver created with session: {driver.session_id}")
        return driver


class FirefoxDriver(Driver):
    def create_driver(self, environment=None, dr_type=None):
        try:
            driver = webdriver.Firefox(options=_init_driver_options(dr_type=dr_type))
            log.info(f"Created Firefox driver with session: {driver.session_id}")
        except Exception as e:
            driver = webdriver.Chrome(
                service=ChromeService(_get_driver_path(dr_type)),
                options=_init_driver_options(dr_type=dr_type),
            )
            log.error(
                f"Failed to create Firefox driver, falling back to Chrome: {e}"
            )
        _configure_driver(driver, environment)
        return driver
