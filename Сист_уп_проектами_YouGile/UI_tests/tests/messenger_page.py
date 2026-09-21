import allure
from playwright.sync_api import Page
from base_page import BasePage


class MessengerPage(BasePage):
    def __init__(self, page: Page, company_id: str) -> None:
        super().__init__(page)
        self.url = f"https://ru.yougile.com/{company_id}/messenger"
        self.new_chat_btn = page.locator("button[aria-label='Новый чат']")
        self.search_input = page.get_by_placeholder("Поиск")
        self.message_input = page.locator("div[contenteditable='true']")
        self.send_btn = page.locator("button:has-text('Отправить')")

    @allure.step("Отправка сообщения пользователю {recipient}: {text}")
    def send_message(self, recipient: str, text: str) -> None:
        self.navigate(self.url)
        self.new_chat_btn.click()
        self.search_input.fill(recipient)
        self.page.get_by_text(recipient).click()
        self.message_input.fill(text)
        self.send_btn.click()

    def is_message_visible(self, text: str) -> bool:
        return self.page.locator(f"text={text}").is_visible()

    @allure.step("Создание группового чата: {group_name}")
    def create_group_chat(self, group_name: str, members: list[str]) -> None:
        self.navigate(self.url)
        self.new_chat_btn.click()
        self.page.get_by_text("Создать группу").click()
        self.page.get_by_placeholder("Название группы").fill(group_name)
        for member in members:
            self.search_input.fill(member)
            self.page.get_by_text(member).click()
        self.page.get_by_role("button", name="Создать").click()

    def is_group_chat_created(self, group_name: str) -> bool:
        return self.page.locator(f"text={group_name}").is_visible()
