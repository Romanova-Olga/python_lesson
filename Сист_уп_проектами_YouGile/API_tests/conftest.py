import json
import pytest
from pathlib import Path
from task_api import TaskAPI
from typing import Generator

CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.json"


@pytest.fixture(scope="session")
def config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def api_client(config: dict) -> TaskAPI:
    return TaskAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        company_id=config["company_id"],
    )


@pytest.fixture(scope="function")
def created_task(api_client: TaskAPI) -> Generator[str, None, None]:
    """Фикстура создает задачу перед тестом и удаляет её после (teardown)."""
    # Для создания задачи нужен columnId.
    # В реальном проекте нужно получить его через API.
    # Здесь для примера используется заглушка.
    column_id = "test-column-id"
    response = api_client.create_task("Временная задача для теста", column_id)

    # Если API не позволяет создать (например, неверный column_id),
    # нужно обработать это или использовать мок. Предположим, успех.
    assert response.status_code == 201, f"Ошибка создания задачи: {response.text}"
    task_id = response.json()["id"]

    yield task_id

    # Teardown: удаляем задачу
    api_client.delete_task(task_id)
