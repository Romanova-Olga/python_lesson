import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Открываем страницу в Google Chrome
driver = webdriver.Chrome()
driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

# 2. В поле ввода #delay вводим значение 45
delay_input = driver.find_element(By.CSS_SELECTOR, "#delay")
delay_input.clear()  # Очищаем поле перед вводом
delay_input.send_keys("45")

# 3. Нажимаем кнопки: 7, +, 8, =
buttons = ["7", "+", "8", "="]
for btn_text in buttons:
    # Ищем кнопку по тексту (используем XPath)
    button = driver.find_element(By.XPATH, f"//span[text()='{btn_text}']")
    button.click()

# 4. Проверяем, что результат 15 появится через 45 секунд
# Ждём, пока элемент с результатом станет видимым и содержащим "15"
# Максимальное время ожидания - 50 секунд (чуть больше 45 для надёжности)
wait = WebDriverWait(driver, 50)
result_element = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".screen"))
)

# Получаем текст результата и проверяем
actual_result = result_element.text
expected_result = "15"

# Делаем assert для проверки
assert actual_result == expected_result, f"Ожидалось {expected_result}, получено {actual_result}"

print("Тест пройден! Результат:", actual_result)

# Закрываем браузер
driver.quit()
