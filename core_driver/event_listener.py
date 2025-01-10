from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


class EventListener(AbstractEventListener):
    """Custom event listener for WebDriver"""

    def after_click(self, element, driver):
        print(f"Clicked on {element.tag_name} at location {element.location}")

    def on_exception(self, exception, driver):
        print(f"Exception occurred: {exception}")
        driver.save_screenshot("exception.png")
