import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from calculator_page import CalculatorPage
import allure


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


@allure.epic("UI Тесты")
@allure.feature("Калькулятор")
@allure.story("Арифметические операции с задержкой")
@allure.title("Проверка операции сложения с задержкой 45 секунд")
@allure.description(
    """
    Тест проверяет работу калькулятора с установленной задержкой:
    1. Устанавливается задержка 45 секунд
    2. Выполняется операция 7 + 8
    3. Проверяется, что результат равен 15
    """
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "calculator", "positive")
@allure.link("https://example.com/calculator", name="Страница калькулятора")
def test_show_calculator_operation(driver):
    """
    Тест проверяет корректность выполнения операции сложения
    с использованием механизма задержки.

    :param driver: WebDriver — экземпляр драйвера от фикстуры.
    :return: None
    """
    # Создаём объект страницы
    calculator_page = CalculatorPage(driver)

    with allure.step("Открытие страницы калькулятора"):
        calculator_page.open()

    with allure.step("Установка задержки 45 секунд"):
        calculator_page.set_delay(45)

    with allure.step("Выполнение операции 7 + 8"):
        calculator_page.click_buttons_sequence(["7", "+", "8", "="])

    with allure.step("Ожидание и получение результата (таймаут 50 секунд)"):
        try:
            result = calculator_page.get_result_value(timeout=50)
        except TimeoutException:
            allure.attach(
                body="Результат не отобразился за 45 секунд",
                name="Ошибка таймаута",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.fail("Результат не отобразился за 45 секунд")

    with allure.step("Проверка, что результат равен 15"):
        assert result == 15, f"Ожидалось значение 15, получено {result}"
