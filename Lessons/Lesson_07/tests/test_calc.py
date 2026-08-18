import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pages.calculator_page import CalculatorPage


@pytest.fixture
def driver():
    """Фикстура для создания и закрытия драйвера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_slow_calculator_operation(driver):
    """
    Тест проверяет работу калькулятора с задержкой:
    1. Устанавливает задержку 45 секунд
    2. Выполняет операцию 7 + 8
    3. Проверяет, что результат равен 15
    """
    # Создаём объект страницы
    calculator_page = CalculatorPage(driver)
    
    # Открываем страницу и выполняем действия
    calculator_page.open()
    calculator_page.set_delay(45)
    calculator_page.click_buttons_sequence(["7", "+", "8", "="])
    
    # Проверяем результат (ждущий до 50 секунд)
    try:
        result = calculator_page.get_result_value(timeout=50)
        assert result == 15, f"Ожидалось значение 15, получено {result}"
    except TimeoutException:
        pytest.fail("Результат не отобразился за 45 секунд")
