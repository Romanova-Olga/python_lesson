"""
Тесты для интернет-магазина SauceDemo с использованием Allure.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from shop_page import LoginPage, InventoryPage, CartPage, CheckoutPage
import allure


@pytest.fixture
def driver():
    """
    Фикстура для создания и закрытия драйвера Firefox.

    Yields:
        WebDriver: Экземпляр драйвера Firefox.
    """
    driver: WebDriver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.epic("UI Тесты")
@allure.feature("Интернет-магазин SauceDemo")
@allure.story("Оформление заказа")
@allure.title("Проверка итоговой суммы в корзине при оформлении заказа")
@allure.description(
    """
    Тест проверяет корректность расчета итоговой суммы при оформлении заказа:
    1. Авторизация на сайте SauceDemo
    2. Добавление трёх товаров в корзину:
       - Sauce Labs Backpack
       - Sauce Labs Bolt T-Shirt
       - Sauce Labs Onesie
    3. Переход в корзину и нажатие кнопки Checkout
    4. Заполнение формы покупателя
    5. Проверка итоговой суммы (ожидается $58.29)
    """
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "saucedemo", "checkout", "positive")
@allure.link("https://www.saucedemo.com/", name="SauceDemo Website")
def test_saucedemo_checkout_total(driver: WebDriver) -> None:
    """
    Тест проверяет итоговую стоимость заказа в интернет-магазине.

    Args:
        driver: WebDriver — экземпляр драйвера от фикстуры.

    Returns:
        None
    """
    with allure.step("1. Открытие сайта и авторизация"):
        login_page: LoginPage = LoginPage(driver).open()
        inventory_page: InventoryPage = login_page.login(
            "standard_user", "secret_sauce")
        allure.attach(
            body="Авторизация выполнена как standard_user",
            name="Авторизация",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("2. Добавление товаров в корзину"):
        inventory_page.add_to_cart("Sauce Labs Backpack") \
            .add_to_cart("Sauce Labs Bolt T-Shirt") \
            .add_to_cart("Sauce Labs Onesie")
        allure.attach(
            body="Добавлены товары: Backpack, Bolt T-Shirt, Onesie",
            name="Товары в корзине",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("3. Переход в корзину и нажатие Checkout"):
        cart_page: CartPage = inventory_page.go_to_cart()
        checkout_page: CheckoutPage = cart_page.click_checkout()

    with allure.step("4. Заполнение формы покупателя"):
        checkout_page.fill_form("Иван", "Петров", "123456")
        allure.attach(
            body="Имя: Иван, Фамилия: Петров, Индекс: 123456",
            name="Данные покупателя",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("5. Чтение итоговой стоимости"):
        total: float = checkout_page.get_total()
        allure.attach(
            body=f"Итоговая сумма: ${total}",
            name="Результат",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("6. Проверка итоговой суммы (ожидается $58.29)"):
        expected_total: float = 58.29
        assert total == expected_total, (
            f"Ожидалось {expected_total}, получено {total}"
        )
        allure.attach(
            body=f"Проверка пройдена: {total} == {expected_total}",
            name="Результат проверки",
            attachment_type=allure.attachment_type.TEXT
        )
