import pytest
from selenium import webdriver
from pages.shop_page import LoginPage
from pages.shop_page import InventoryPage
from pages.shop_page import CartPage
from pages.shop_page import CheckoutPage


def test_saucedemo_checkout_total():
    driver = webdriver.Firefox()
    try:
        # 1. Открыть сайт и авторизоваться
        login_page = LoginPage(driver).open()
        inventory_page = login_page.login("standard_user", "secret_sauce")

        # 2. Добавить товары в корзину
        inventory_page.add_to_cart("Sauce Labs Backpack") \
                      .add_to_cart("Sauce Labs Bolt T-Shirt") \
                      .add_to_cart("Sauce Labs Onesie")

        # 3. Перейти в корзину и нажать Checkout
        cart_page = inventory_page.go_to_cart()
        checkout_page = cart_page.click_checkout()

        # 4. Заполнить форму (замените на свои данные)
        checkout_page.fill_form("Иван", "Петров", "123456")

        # 5. Прочитать итоговую стоимость
        total = checkout_page.get_total()

        # 6. Проверить, что итоговая сумма равна $58.29
        assert total == 58.29, f"Expected 58.29, but got {total}"

    finally:
        # 7. Закрыть браузер
        driver.quit()
