import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions


@pytest.fixture
def driver():
    # Настройка Edge (можно заменить на Safari, но для автоматизации лучше Edge/Chrome)
    options = EdgeOptions()
    options.add_argument("--headless")  # Уберите, если хотите видеть браузер
    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_data_types_form(driver):
    # 1. Открыть страницу
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

    # 2. Заполнить форму
    fields = {
        "first-name": "Иван",
        "last-name": "Петров",
        "address": "Ленина, 55-3",
        "e-mail": "test@skypro.com",
        "phone": "+798589999878",
        "zip-code": "",  # оставляем пустым
        "city": "Москва",
        "country": "Россия",
        "job-position": "QA",
        "company": "SkyPro"
    }

    for name, value in fields.items():
        input_field = driver.find_element(By.NAME, name)
        input_field.clear()
        if value:
            input_field.send_keys(value)

    # 3. Нажать Submit
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Ожидание появления подсветки (можно небольшой таймаут)
    wait = WebDriverWait(driver, 5)

    # 4. Проверить, что Zip code подсвечен красным (class содержит 'is-invalid')
    zip_field = driver.find_element(By.NAME, "zip-code")
    wait.until(EC.presence_of_element_located((By.NAME, "zip-code")))
    assert "is-invalid" in zip_field.get_attribute("class"), "Zip code should be highlighted red"

    # 5. Проверить, что остальные поля подсвечены зеленым (class содержит 'is-valid')
    green_fields = [
        "first-name", "last-name", "address", "e-mail",
        "phone", "city", "country", "job-position", "company"
    ]
    for name in green_fields:
        field = driver.find_element(By.NAME, name)
        # Иногда класс появляется с задержкой, ждем
        wait.until(lambda d: "is-valid" in field.get_attribute("class"))
        assert "is-valid" in field.get_attribute("class"), f"Field {name} should be highlighted green"

    # 6. Закрываем браузер **в конце работы** (так требует ДЗ)
