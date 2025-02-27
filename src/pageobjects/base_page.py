from enum import Enum
from typing import Tuple, Optional, Literal
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException

from utils.helpers import timing
from utils.logger import log

# Type alias for locators
Locator = Tuple[str, str]


class WaitType(Enum):
    DEFAULT = 20
    SHORT = 5
    LONG = 60
    FLUENT = 10


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(driver, WaitType.DEFAULT.value)
        self._short_wait = WebDriverWait(driver, WaitType.SHORT.value)
        self._long_wait = WebDriverWait(driver, WaitType.LONG.value)
        self._fluent_wait = WebDriverWait(
            driver,
            WaitType.FLUENT.value,
            poll_frequency=1,
            ignored_exceptions=[ElementNotVisibleException],
        )

    def _get_waiter(self, wait_type: Optional[WaitType] = None) -> WebDriverWait:
        """
        Returns the appropriate WebDriverWait object based on the wait_type.
        Defaults to the default wait if no wait_type is provided.
        """
        return {
            WaitType.SHORT: self._short_wait,
            WaitType.LONG: self._long_wait,
            WaitType.FLUENT: self._fluent_wait,
        }.get(wait_type, self._wait)

    @timing
    def wait_for(
        self,
        locator: Locator,
        condition: Literal["clickable", "visible", "present"] = "visible",
        waiter: Optional[WebDriverWait] = None,
    ) -> WebElement:
        """Wait for an element"""
        waiter = waiter or self._wait

        conditions = {
            "clickable": ec.element_to_be_clickable(locator),
            # Pass the locator tuple as a single argument
            "visible": ec.visibility_of_element_located(locator),
            "present": ec.presence_of_element_located(locator),
        }

        if condition not in conditions:
            raise ValueError(f"Unknown condition: {condition}")

        try:
            return waiter.until(conditions[condition])
        except TimeoutException as e:
            raise TimeoutException(
                f"Condition '{condition}' failed for element {locator} "
                f"after {waiter._timeout} seconds"
            ) from e

    def click(
        self,
        locator: Locator,
        condition: Literal["clickable", "visible", "present"] = "clickable",
        wait_type: Optional[WaitType] = None,
    ):
        """
        Click on an element.
        """
        waiter = self._get_waiter(wait_type)
        element = self.wait_for(locator, condition=condition, waiter=waiter)
        element.click()

    # @log()
    # @timing
    def set(self, locator: Locator, text: str, wait_type: Optional[WaitType] = None):
        """
        Set text in an input field.
        """
        waiter = self._get_waiter(wait_type)
        element = self.wait_for(locator, waiter=waiter)
        element.clear()
        element.send_keys(text)

    @log
    def get_text(
        self, locator: Locator, wait_type: Optional[WaitType] = None
    ) -> str:
        """
        Get the text of an element.
        """
        waiter = self._get_waiter(wait_type)
        return self.wait_for(locator, condition="present", waiter=waiter).text

    @log()
    def get_title(self) -> str:
        """
        Get the page title.
        """
        return self.driver.title

    def navigate_to(self, url):
        """Navigate to a specific URL."""
        self.driver.get(url)

    def get_current_url(self):
        """Get the current URL of the page."""
        return self.driver.current_url

    def refresh(self):
        """Refresh the current page."""
        self.driver.refresh()

    def scroll_to_element(self, element):
        """Sroll to element"""
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
