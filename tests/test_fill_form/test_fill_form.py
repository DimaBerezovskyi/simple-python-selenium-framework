import time

import pytest
from src.pageobjects.text.fill_form import FillForm
from utils.crypto import Secure
from utils.yaml_reader import YAMLReader


@pytest.fixture
def get_password():
    secure = Secure()
    read = YAMLReader.read("data.yaml", to_simple_namespace=True)
    password = read.users.john.details.password
    return secure.decrypt_password(password)


class TestFillForm:
    def test_fill_user(self, make_driver, get_password):
        fill = FillForm(make_driver)

        # Use the password provided by the fixture
        password = get_password
        fill.enter_username("selenium framework")
        fill.enter_password(password)
