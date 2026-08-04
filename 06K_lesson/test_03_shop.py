import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class TestSauceDemo:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Настройка браузера Firefox перед каждым тестом"""
        options = Options()
        options.add_argument("--headless")  # Опционально: запуск без GUI
        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def test_total_price(self):
        """Тест проверки итоговой стоимости в корзине"""
        # 1. Откройте сайт магазина в Firefox
        self.driver.get("https://www.saucedemo.com/")

        # 2. Авторизуйтесь как пользователь standard_user
        username = self.wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        username.send_keys("standard_user")
        password = self.driver.find_element(By.ID, "password")
        password.send_keys("secret_sauce")
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()

        # Проверка успешной авторизации
        self.wait.until(EC.url_contains("inventory.html"))

        # 3. Добавьте в корзину товары
        items_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        # Получаем все товары на странице
        inventory_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")

        for item in inventory_items:
            item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if item_name in items_to_add:
                add_button = item.find_element(By.XPATH, ".//button[contains(@id, 'add-to-cart')]")
                add_button.click()

        # 4. Перейдите в корзину
        cart_link = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        self.wait.until(EC.url_contains("cart.html"))

        # 5. Нажмите Checkout
        checkout_button = self.driver.find_element(By.ID, "checkout")
        checkout_button.click()
        self.wait.until(EC.url_contains("checkout-step-one.html"))

        # 6. Заполните форму своими данными
        first_name = self.driver.find_element(By.ID, "first-name")
        first_name.send_keys("Иван")
        last_name = self.driver.find_element(By.ID, "last-name")
        last_name.send_keys("Иванов")
        postal_code = self.driver.find_element(By.ID, "postal-code")
        postal_code.send_keys("123456")

        # 7. Нажмите кнопку Continue
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        self.wait.until(EC.url_contains("checkout-step-two.html"))

        # 8. Прочитайте со страницы итоговую стоимость (Total)
        total_element = self.driver.find_element(By.CLASS_NAME, "summary_total_label")
        total_text = total_element.text
        total_value = float(total_text.split("$")[1])

        # 10. Проверьте, что итоговая сумма равна $58.29
        expected_total = 58.29
        assert total_value == expected_total, \
            f"Итоговая сумма {total_value} не равна ожидаемой {expected_total}"

        # 9. Закройте браузер (автоматически через фикстуру)