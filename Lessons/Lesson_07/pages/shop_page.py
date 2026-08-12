import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# === Page Object: Login Page ===
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def open(self):
        self.driver.get("https://www.saucedemo.com/")
        return self

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
        return InventoryPage(self.driver)


# === Page Object: Inventory (Main) Page ===
class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_to_cart_buttons = {
            "Sauce Labs Backpack": (By.ID, "add-to-cart-sauce-labs-backpack"),
            "Sauce Labs Bolt T-Shirt": (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"),
            "Sauce Labs Onesie": (By.ID, "add-to-cart-sauce-labs-onesie"),
        }
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")

    def add_to_cart(self, product_name):
        if product_name in self.add_to_cart_buttons:
            self.driver.find_element(*self.add_to_cart_buttons[product_name]).click()
        return self

    def go_to_cart(self):
        self.driver.find_element(*self.cart_icon).click()
        return CartPage(self.driver)


# === Page Object: Cart Page ===
class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkout_button = (By.ID, "checkout")

    def click_checkout(self):
        self.driver.find_element(*self.checkout_button).click()
        return CheckoutPage(self.driver)


# === Page Object: Checkout Page ===
class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.total_label = (By.CLASS_NAME, "summary_total_label")

    def fill_form(self, first_name, last_name, postal_code):
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.postal_code_input).send_keys(postal_code)
        self.driver.find_element(*self.continue_button).click()
        return self

    def get_total(self):
        # Wait for total to appear and extract number
        total_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.total_label)
        )
        total_text = total_element.text
        # Example: "Total: $58.29" -> 58.29
        return float(total_text.split("$")[1])
