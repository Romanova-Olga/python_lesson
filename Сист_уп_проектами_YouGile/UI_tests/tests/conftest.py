import json
import pytest
from pathlib import Path
from typing import Generator
from typing import Iterator
from playwright.sync_api import Page, sync_playwright, Browser, BrowserContext

CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.json"


@pytest.fixture(scope="session")
def config() -> dict:
    """Загружает конфигурацию."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def browser_instance() -> Generator[Browser, None, None]:
    """Запуск браузера."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def auth_context(browser_instance: Browser, config: dict) -> Iterator[BrowserContext]:
    """
    Создает контекст с авторизацией.
    Использует API-ключ для получения токена и подстановки его в LocalStorage/Cookies.
    """
    context = browser_instance.new_context()
    page = context.new_page()

    # Быстрый вход через UI (для примера),
    # в реальном проекте лучше использовать API для получения токена
    page.goto(config["base_url"])

    # Логин (селекторы условные, нужно уточнить через DevTools YouGile)
    page.get_by_placeholder("Email").fill(config["login"])
    page.get_by_role("button", name="Войти").click()
    page.get_by_placeholder("Пароль").fill(config["password"])
    page.get_by_role("button", name="Войти").click()

    # Ожидание загрузки рабочего пространства
    page.wait_for_url(f"**/{config['company_id']}/**")

    # Сохраняем состояние авторизации
    context.storage_state(path="auth_state.json")
    page.close()

    yield context
    context.close()


@pytest.fixture(scope="function")
def page(auth_context: BrowserContext) -> Iterator[Page]:
    """Создает новую страницу для каждого теста с уже выполненной авторизацией."""
    page = auth_context.new_page()
    page.set_default_timeout(15000)
    yield page
    page.close()
