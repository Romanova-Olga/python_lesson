import allure
from playwright.sync_api import Page
from base_page import BasePage


class KanbanPage(BasePage):
    def __init__(self, page: Page, company_id: str) -> None:
        super().__init__(page)
        self.url = f"https://ru.yougile.com/{company_id}/boards"
        self.add_task_btn = page.locator("button:has-text('Добавить задачу')").first
        self.task_title_input = page.locator("textarea[placeholder='Введите название']")
        self.save_btn = page.locator("button:has-text('Сохранить')")
        self.task_cards = page.locator(".task-card")  # Условный селектор

    @allure.step("Создание задачи с названием: {title}")
    def create_task(self, title: str) -> None:
        self.navigate(self.url)
        self.add_task_btn.click()
        self.task_title_input.fill(title)
        self.save_btn.click()

    def is_task_visible(self, title: str) -> bool:
        return self.task_cards.filter(has_text=title).is_visible()
