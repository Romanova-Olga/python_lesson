import allure
import pytest
from playwright.sync_api import Page
from kanban_page import KanbanPage
from messenger_page import MessengerPage
from sales_funnel_page import SalesFunnelPage
from base_page import BasePage


@allure.epic("YouGile UI Автоматизация")
@allure.feature("Ключевые бизнес-сценарии")
class TestYouGileScenarios:

    @pytest.fixture(autouse=True)
    def setup(self, config: dict) -> None:
        """Автоматически передает company_id в тесты, если нужно."""
        self.company_id = config["company_id"]

    @allure.title("Создание задачи на канбан-доске")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_task_on_kanban_board(self, page: Page) -> None:
        """Сценарий 1: Создание задачи на канбан-доске."""
        kanban = KanbanPage(page, self.company_id)
        task_title = "Автотест: Проверка канбана"

        kanban.create_task(task_title)

        with allure.step(f"Проверка, что задача '{task_title}' отображается"):
            assert kanban.is_task_visible(task_title), "Задача не найдена на доске!"

    @allure.title("Отправка текстового сообщения в мессенджере")
    def test_send_text_message_in_messenger(self, page: Page) -> None:
        """Сценарий 2: Корпоративный мессенджер. Отправка текстового сообщения."""
        messenger = MessengerPage(page, self.company_id)
        recipient = "Иван Иванов"  # Имя пользователя в вашей компании
        message_text = "Привет! Это тестовое сообщение от автотеста."

        messenger.send_message(recipient, message_text)

        with allure.step("Проверка отправки сообщения"):
            assert messenger.is_message_visible(
                message_text
            ), "Сообщение не отправилось!"

    @allure.title("Создание группового чата")
    def test_create_group_chat(self, page: Page) -> None:
        """Сценарий 3: Создание группового чата."""
        messenger = MessengerPage(page, self.company_id)
        group_name = "Группа тестировщиков"
        members = ["Иван Иванов", "Мария Петрова"]

        messenger.create_group_chat(group_name, members)

        with allure.step("Проверка создания группового чата"):
            assert messenger.is_group_chat_created(
                group_name
            ), "Групповой чат не создан!"

    @allure.title("Создание сделки в воронке продаж")
    def test_create_deal_in_sales_funnel(self, page: Page) -> None:
        """Сценарий 4: Создание сделки в воронке продаж."""
        funnel = SalesFunnelPage(page, self.company_id)
        deal_name = "Сделка №999 (Автотест)"
        deal_amount = "150000"

        funnel.create_deal(deal_name, deal_amount)

        with allure.step("Проверка появления сделки в воронке"):
            assert funnel.is_deal_in_funnel(deal_name), "Сделка не появилась в воронке!"

    @allure.title("Проверка успешной авторизации (Базовая проверка)")
    def test_successful_authorization(self, page: Page, config: dict) -> None:
        """Сценарий 5: Проверка входа в систему (замена сценария регистрации, так как есть готовые креды)."""
        base = BasePage(page)
        base.navigate(f"https://ru.yougile.com/{self.company_id}/boards")

        with allure.step(
            "Проверка, что пользователь авторизован (виден аватар или название компании)"
        ):
            # Условный селектор, нужно уточнить в реальном DOM
            avatar = page.locator("button[aria-label='Профиль']").first
            assert avatar.is_visible(), "Пользователь не авторизован!"
