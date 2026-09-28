import allure
from playwright.sync_api import Page
from base_page import BasePage


class KanbanPage(BasePage):
    def __init__(self, page: Page, company_id: str) -> None:
        super().__init__(page)
        self.url = f"https://ru.yougile.com/{company_id}/boards"
        self.add_task_btn = page.get_by_text("Добавить задачу").first
        self.task_title_input = page.get_by_placeholder("Введите название задачи...")

    @allure.step("Создание задачи с названием: {title}")
    def create_task(self, title: str) -> None:
        self.navigate(self.url)
        self.add_task_btn.click()
        self.task_title_input.fill(title)
        self.task_title_input.press("Enter")

    def is_task_visible(self, title: str) -> bool:
        return self.page.get_by_text(title).is_visible()
