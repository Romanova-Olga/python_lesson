import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_slow_calculator(driver):
    # 1. Открыть страницу
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

    # 2. Ввести значение 45 в поле задержки
    delay_input = driver.find_element(By.CSS_SELECTOR, "#delay")
    delay_input.clear()
    delay_input.send_keys("45")

    # 3. Нажать кнопки: 7, +, 8, =
    driver.find_element(By.XPATH, "//span[text()='7']").click()
    driver.find_element(By.XPATH, "//span[text()='+']").click()
    driver.find_element(By.XPATH, "//span[text()='8']").click()
    driver.find_element(By.XPATH, "//span[text()='=']").click()

    # 4. Проверить, что через 45 секунд отобразится результат 15
    try:
        # Ждём до 50 секунд (45 + запас), чтобы результат появился
        result_element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".screen"))
        )
        # Получаем текст результата и преобразуем в число
        result_text = result_element.text.strip()
        assert result_text == "15", f"Ожидалось '15', получено '{result_text}'"
    except TimeoutException:
        pytest.fail("Результат не отобразился за 45 секунд")
