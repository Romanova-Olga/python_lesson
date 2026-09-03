import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    """
    Фикстура для создания и закрытия драйвера.

    :return: WebDriver — экземпляр драйвера Chrome.
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
