from selenium import webdriver
from selenium.webdriver.common.by import By


def test_form_submission():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.org/forms/post")

    # Находим поле ввода по атрибуту name="custname" и вводим имя
    name_field = driver.find_element(By.NAME, "custname")
    name_field.send_keys("Ольга Ро")

    # Находим кнопку Submit по тексту и нажимаем
    submit_button = driver.find_element(By.XPATH, "//button[text()='Submit']")
    submit_button.click()

    # Проверяем, что URL изменился
    assert driver.current_url == "https://httpbin.org/post", "URL не изменился"

    driver.quit()
    