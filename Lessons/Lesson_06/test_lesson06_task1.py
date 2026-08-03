from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_dygnamic_loading():
    driver = webdriver.Chrome()

    # 1. Откройте страницу https://the-internet.herokuapp.com/dynamic_loading/2
    driver.maximize_window()
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

    # 2. Найдите и нажмите на кнопку "Start"
    start_button=driver.find_element(By.ID,"start")
    driver.execute_script("arguments[0].click();",start_button)

    # 3. Дождитесь появления текста "Hello World!"
    WebDriverWait(driver,30).until(
        EC.text_to_be_present_in_element((By.ID,"finish"),"Hello World!")
    )

    element=driver.find_element(By.ID,"finish")

    # 4. Сделайте скриншот страницы
    driver.save_screenshot("result.png")

    # 5. Проверьте, что появившийся текст равен "Hello World!"
    assert element.text=="Hello World!",f"Получен текст:{element.text}"

    driver.quit()
