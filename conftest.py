import pytest
import os

from dotenv import load_dotenv
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from core_driver.event_listener import EventListener
from core_driver.driver_factory import WebDriverFactory
from utils.logger import Logger, LogLevel

log = Logger(log_lvl=LogLevel.INFO).get_instance()


def event_listener(driver) -> EventFiringWebDriver:
    """Attach the event listener to the driver."""
    e_driver: EventFiringWebDriver = EventFiringWebDriver(driver, EventListener())
    return e_driver


@pytest.fixture(params=["local", "firefox"])
def driver_types(request):
    # To run tests on several browsers, we can pass the driver_types fixture as
    # a parameter to the fixture make_drive
    return request.param


@pytest.fixture
def make_driver(request) -> EventFiringWebDriver:
    load_dotenv(dotenv_path=f"{request.config.getoption('--env')}")
    env = request.config.getoption("--env")
    dr_type = request.config.getoption("--type")
    driver = None

    def _make_driver() -> EventFiringWebDriver:
        nonlocal driver
        # Create WebDriver instance
        driver = WebDriverFactory().create_driver(
            environment=env, driver_type=dr_type
        )
        # Attach event listener
        driver_with_listener = event_listener(driver)
        return driver_with_listener

    driver_instance = _make_driver()

    yield driver_instance

    # Teardown code to quit the driver
    if driver is not None:
        driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--browser-version",
        action="store",
        default="129",
        help="Specify the browser version",
    )
    parser.addoption(
        "--env", action="store", default="stage", help="Run browser in headless mode"
    )
    parser.addoption(
        "--type", action="store", default="local", help="Run browser in os type"
    )


def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure."""
    if call.excinfo is not None:
        # Make sure the driver is being captured correctly
        driver = item.funcargs.get("make_driver", None)

        if driver is not None:
            screenshot_dir = "reports/screenshots"
            os.makedirs(
                screenshot_dir, exist_ok=True
            )  # Create directory if it does not exist
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")

            try:
                driver.save_screenshot(screenshot_path)
                log.info(f"Screenshot saved to: {screenshot_path}")
            except Exception as e:
                log.error(f"Failed to save screenshot: {e}")
        else:
            log.error("Driver instance is not available for capturing screenshot.")
