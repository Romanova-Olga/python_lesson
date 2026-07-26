from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_navigation():
    driver = webdriver.Chrome()

    # Шаг 1: Откройте страницу https://httpbin.org/
    driver.get("https://httpbin.org/")
    sleep(3)
    
    # Шаг 2: Найдите и кликните на ссылку HTML Form
    html_form_link = driver.find_element(By.LINK_TEXT, "HTML Form")
    html_form_link.click()
    
    # Шаг 3: Проверьте, что URL изменился на /forms/post
    expected_url = "https://httpbin.org/forms/post"
    actual_url = driver.current_url
    assert actual_url == expected_url, f"Ожидался URL {expected_url}, получен {actual_url}"
    
    # Шаг 4: Вернитесь назад на главную страницу
    driver.back()
    sleep(3)
    
    # Шаг 5: Проверьте, что вернулись на исходный URL
    initial_url = "https://httpbin.org/"
    current_url = driver.current_url
    assert current_url == initial_url, f"Ожидался URL {initial_url}, получен {current_url}"

    driver.quit()
