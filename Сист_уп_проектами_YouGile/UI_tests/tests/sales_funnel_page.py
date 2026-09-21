import allure
from playwright.sync_api import Page
from base_page import BasePage


class SalesFunnelPage(BasePage):
    def __init__(self, page: Page, company_id: str) -> None:
        super().__init__(page)
        self.url = f"https://ru.yougile.com/{company_id}/crm"
        self.add_deal_btn = page.locator("button:has-text('Добавить сделку')")
        self.deal_name_input = page.get_by_placeholder("Название сделки")
        self.amount_input = page.get_by_placeholder("Сумма")

    @allure.step("Создание сделки '{name}' на сумму {amount}")
    def create_deal(self, name: str, amount: str) -> None:
        self.navigate(self.url)
        self.add_deal_btn.click()
        self.deal_name_input.fill(name)
        self.amount_input.fill(amount)
        self.page.get_by_role("button", name="Сохранить").click()

    def is_deal_in_funnel(self, name: str) -> bool:
        return self.page.locator(f".deal-card:has-text('{name}')").is_visible()
