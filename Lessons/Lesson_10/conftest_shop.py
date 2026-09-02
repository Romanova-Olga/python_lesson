"""
Конфигурационный файл для pytest.
Содержит общие фикстуры и настройки.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для создания и закрытия драйвера Firefox.

    Returns:
        WebDriver: Экземпляр драйвера Firefox.
    """
    driver: WebDriver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()
