from selenium.webdriver.common.by import By


class General:
    LOGO = (By.ID, "userForm")
    ELEMENTS = (By.XPATH, "//h5[text()='Elements']")
    FORMS = (By.XPATH, "//div[@class='card-body']//h5[text()='Forms']")
    STORE = (By.XPATH, "//h5[text()='Book Store Application']")


class TextBoxFields:
    USER_NAME = (By.ID, "userName")
    TEXT_BOX = (By.XPATH, "//span[text()='Text Box']")
