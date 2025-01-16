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


def _get_project_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _get_driver_path(driver_type):
    if not driver_type:
        ErrorHandler.raise_error(ErrorType.UNSUPPORTED_DRIVER_TYPE)

    driver_path = os.path.join(_get_project_dir(), "resources", driver_type)

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
        try:
            caps = YAMLReader.read_caps(browser)
            log.info(f"Capabilities for {browser} driver: {caps}")
            return caps
        except Exception as e:
            log.error(f"Error reading capabilities for {browser}: {e}")
            ErrorHandler.raise_error(ErrorType.CAPABILITY_NOT_FOUND, browser)


class LocalDriver(Driver):
    def create_driver(self, environment=None, dr_type="chromedriver"):
        driver = None
        options = _init_driver_options(dr_type=dr_type)
        try:
            driver_path = ChromeDriverManager().install()
            driver = webdriver.Chrome(
                service=ChromeService(executable_path=driver_path),
                options=options
            )
            log.info(f"Local Chrome driver created with session: {driver.session_id}")
        except Exception as e:
            log.error(f"ChromeDriverManager failed, falling back to local driver: {e}")
            driver = webdriver.Chrome(
                service=ChromeService(_get_driver_path(dr_type)),
                options=options
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
    def create_driver(self, environment=None, dr_type="firefox"):
        driver = None
        options = _init_driver_options(dr_type=dr_type)
        try:
            driver = webdriver.Firefox(options=options)
            log.info(f"Firefox driver created with session: {driver.session_id}")
        except Exception as e:
            log.error(f"Failed to create Firefox driver, falling back to Chrome: {e}")
            driver = webdriver.Chrome(
                service=ChromeService(_get_driver_path("chromedriver")),
                options=options
            )
        _configure_driver(driver, environment)
        return driver
