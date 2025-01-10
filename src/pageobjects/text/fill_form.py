from src.locators.locators import TextBoxFields, General
from src.pageobjects.base_page import BasePage
from utils.logger import log


class FillForm(BasePage):
    @log()
    def enter_username(self, name: str):
        """Enter username"""
        self.set(TextBoxFields.USER_NAME, name)

    @log()
    def enter_password(self, password):
        """Enter password"""
        self.set(TextBoxFields.USER_NAME, password)
