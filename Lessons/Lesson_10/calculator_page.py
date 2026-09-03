from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    """Класс Page Object для страницы калькулятора."""

    def __init__(self, driver):
        """
        Инициализация страницы калькулятора.

        :param driver: WebDriver — экземпляр драйвера Selenium.
        """
        self.driver = driver
        self.url = (
            "https://bonigarcia.dev/"
            "selenium-webdriver-java/"
            "slow-calculator.html"
        )

        # Локаторы
        self.delay_input_locator = (By.CSS_SELECTOR, "#delay")
        self.result_screen_locator = (By.CSS_SELECTOR, ".screen")
        self.button_locator_template = "/span[text()='{}']"

    def open(self):
        """
        Открыть страницу калькулятора.

        :return: CalculatorPage — текущий экземпляр для цепочки вызовов.
        """
        self.driver.get(self.url)
        return self

    def set_delay(self, seconds):
        """
        Установить задержку в поле ввода.

        :param seconds: int или str — количество секунд задержки.
        :return: CalculatorPage — текущий экземпляр для цепочки вызовов.
        """
        delay_input = self.driver.find_element(*self.delay_input_locator)
        delay_input.clear()
        delay_input.send_keys(str(seconds))
        return self

    def click_button(self, button_text):
        """
        Нажать на кнопку калькулятора по её тексту.

        :param button_text: str — текст на кнопке.
        :return: CalculatorPage — текущий экземпляр для цепочки вызовов.
        """
        button_locator = (By.XPATH, f"//span[text()='{button_text}']")
        button = self.driver.find_element(*button_locator)
        button.click()
        return self

    def click_buttons_sequence(self, buttons):
        """
        Нажать последовательность кнопок.

        :param buttons: list[str] — список текстов кнопок для нажатия.
        :return: CalculatorPage — текущий экземпляр для цепочки вызовов.
        """
        for button in buttons:
            self.click_button(button)
        return self

    def get_result_text(self, timeout=50):
        """
        Получить текст результата с ожиданием.

        :param timeout: int — максимальное время ожидания в секундах.
        :return: str — текст результата.
        """
        result_element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.result_screen_locator)
        )
        return result_element.text.strip()

    def get_result_value(self, timeout=50):
        """
        Получить результат в виде числа.

        :param timeout: int — максимальное время ожидания в секундах.
        :return: int или float или str — результат в числовом формате.
        """
        text = self.get_result_text(timeout)
        try:
            return float(text) if '.' in text else int(text)
        except ValueError:
            return text
