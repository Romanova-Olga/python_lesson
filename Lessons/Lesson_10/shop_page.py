"""
Page Object модели для сайта SauceDemo.
Содержит классы для работы со страницами:
логин, инвентарь, корзина, оформление заказа.
"""

from typing import Dict, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


# === Page Object: Login Page ===
class LoginPage:
    """
    Page Object для страницы авторизации.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы логина.

        Args:
            driver: Экземпляр WebDriver.
        """
        self.driver: WebDriver = driver
        self.username_input: Tuple[str, str] = (By.ID, "user-name")
        self.password_input: Tuple[str, str] = (By.ID, "password")
        self.login_button: Tuple[str, str] = (By.ID, "login-button")

    def open(self) -> "LoginPage":
        """
        Открывает страницу авторизации.

        Returns:
            LoginPage: Текущий экземпляр страницы для цепочки вызовов.
        """
        self.driver.get("https://www.saucedemo.com/")
        return self

    def login(self, username: str, password: str) -> "InventoryPage":
        """
        Выполняет авторизацию на сайте.

        Args:
            username: Имя пользователя.
            password: Пароль.

        Returns:
            InventoryPage: Страница инвентаря после успешного входа.
        """
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
        return InventoryPage(self.driver)


# === Page Object: Inventory (Main) Page ===
class InventoryPage:
    """
    Page Object для главной страницы (инвентарь).
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы инвентаря.

        Args:
            driver: Экземпляр WebDriver.
        """
        self.driver: WebDriver = driver
        self.add_to_cart_buttons: Dict[str, Tuple[str, str]] = {
            "Sauce Labs Backpack": (
                By.ID, "add-to-cart-sauce-labs-backpack"),
            "Sauce Labs Bolt T-Shirt": (
                By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"),
            "Sauce Labs Onesie": (
                By.ID, "add-to-cart-sauce-labs-onesie"),
        }
        self.cart_icon: Tuple[str, str] = (By.CLASS_NAME, "shopping_cart_link")

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        """
        Добавляет товар в корзину по имени.

        Args:
            product_name: Название товара.

        Returns:
            InventoryPage: Текущий экземпляр страницы для цепочки вызовов.
        """
        if product_name in self.add_to_cart_buttons:
            self.driver.find_element(
                *self.add_to_cart_buttons[product_name]).click()
        return self

    def go_to_cart(self) -> "CartPage":
        """
        Переходит в корзину.

        Returns:
            CartPage: Страница корзины.
        """
        self.driver.find_element(*self.cart_icon).click()
        return CartPage(self.driver)


# === Page Object: Cart Page ===
class CartPage:
    """
    Page Object для страницы корзины.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы корзины.

        Args:
            driver: Экземпляр WebDriver.
        """
        self.driver: WebDriver = driver
        self.checkout_button: Tuple[str, str] = (By.ID, "checkout")

    def click_checkout(self) -> "CheckoutPage":
        """
        Нажимает кнопку оформления заказа.

        Returns:
            CheckoutPage: Страница оформления заказа.
        """
        self.driver.find_element(*self.checkout_button).click()
        return CheckoutPage(self.driver)


# === Page Object: Checkout Page ===
class CheckoutPage:
    """
    Page Object для страницы оформления заказа.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы оформления заказа.

        Args:
            driver: Экземпляр WebDriver.
        """
        self.driver: WebDriver = driver
        self.first_name_input: Tuple[str, str] = (By.ID, "first-name")
        self.last_name_input: Tuple[str, str] = (By.ID, "last-name")
        self.postal_code_input: Tuple[str, str] = (By.ID, "postal-code")
        self.continue_button: Tuple[str, str] = (By.ID, "continue")
        self.total_label: Tuple[str, str] = (
            By.CLASS_NAME, "summary_total_label")

    def fill_form(
            self,
            first_name: str,
            last_name: str,
            postal_code: str
         ) -> "CheckoutPage":
        """
        Заполняет форму покупателя и нажимает Continue.

        Args:
            first_name: Имя покупателя.
            last_name: Фамилия покупателя.
            postal_code: Почтовый индекс.

        Returns:
            CheckoutPage: Текущий экземпляр страницы для цепочки вызовов.
        """
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(
            *self.postal_code_input
        ).send_keys(postal_code)
        self.driver.find_element(*self.continue_button).click()
        return self

    def get_total(self) -> float:
        """
        Получает итоговую сумму заказа.

        Returns:
            float: Итоговая сумма в виде числа с плавающей точкой.
        """
        total_element: WebElement = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.total_label)
        )
        total_text: str = total_element.text
        # Example: "Total: $58.29" -> 58.29
        return float(total_text.split("$")[1])
