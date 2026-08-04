from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка Firefox (без головного режима, чтобы видеть процесс)
options = Options()
options.headless = False  # Можно изменить на True, если не нужно визуальное выполнение

# Инициализация драйвера
driver = webdriver.Firefox(options=options)

try:
    # 1. Откройте сайт магазина
    driver.get("https://www.saucedemo.com/")

    # 2. Авторизуйтесь как standard_user
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Ожидание загрузки страницы товаров
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

    # 3. Добавьте в корзину товары
    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie"
    ]

    for item_name in items_to_add:
        # Находим элемент товара по имени
        item = driver.find_element(By.XPATH, f"//div[text()='{item_name}']")
        add_button = item.find_element(By.XPATH, "./ancestor::div[@class='inventory_item']//button[contains(@class, 'btn_inventory')]")
        add_button.click()

    # 4. Перейдите в корзину
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Ожидание загрузки страницы корзины
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))

    # 5. Нажмите Checkout
    driver.find_element(By.ID, "checkout").click()

    # Ожидание загрузки формы оформления заказа
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "first-name")))

    # 6. Заполните форму своими данными
    driver.find_element(By.ID, "first-name").send_keys("Иван")
    driver.find_element(By.ID, "last-name").send_keys("Петров")
    driver.find_element(By.ID, "postal-code").send_keys("123456")

    # 7. Нажмите кнопку Continue
    driver.find_element(By.ID, "continue").click()

    # Ожидание загрузки страницы подтверждения заказа
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))

    # 8. Прочитайте итоговую стоимость (Total)
    total_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
    total_text = total_element.text  # Например: "Total: $58.29"
    total_value = total_text.replace("Total: ", "")

    # 9. Закройте браузер
    driver.quit()

    # 10. Проверьте, что итоговая сумма равна $58.29
    expected_total = "$58.29"
    if total_value == expected_total:
        print(f"✅ Проверка пройдена! Итоговая сумма: {total_value}")
    else:
        print(f"❌ Ошибка! Ожидалось {expected_total}, получено {total_value}")

except Exception as e:
    print(f"❌ Произошла ошибка: {e}")
    driver.quit()
