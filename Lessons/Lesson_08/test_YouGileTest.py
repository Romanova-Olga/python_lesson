import pytest
import requests

from YouGile_Api import ProjectsAPI
from YouGile_Api import AuthAPI

def test_create_project(api_with_token):
    title = "Старый проект"
    
    response = api_with_token.create_project(title)
    
    # Проверка статус-кода
    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
    
    # Проверка структуры ответа
    result = response.json()
    assert result is not None
    assert "id" in result, "Ответ не содержит 'id'"
    assert result["id"] is not None
    assert "title" in result, "Ответ не содержит 'title'"
    assert result["title"] == title
    assert "companyId" in result, "Ответ не содержит 'companyId'"
    assert "createdAt" in result, "Ответ не содержит 'createdAt'"
    assert "createdBy" in result, "Ответ не содержит 'createdBy'"
    assert "users" in result, "Ответ не содержит 'users'"
    assert isinstance(result["users"], list), "users должен быть списком"
    
    print(f"✅ Проект создан с ID: {result['id']}")


def test_update_project(api_with_token):
    """Тест обновления проекта с проверкой статус-кода"""
    old_title = "Старый проект"
    new_title = "Новый проект"
    
    # Создание проекта
    create_response = api_with_token.create_project(old_title)
    assert create_response.status_code == 201
    created_project = create_response.json()
    project_id = created_project["id"]
    
    # Обновление проекта
    update_response = api_with_token.update_project(project_id, new_title)
    
    # Проверка статус-кода
    assert update_response.status_code == 200, f"Ожидался статус 200, получен {update_response.status_code}"
    
    # Проверка структуры ответа
    updated_project = update_response.json()
    assert updated_project is not None
    assert updated_project["id"] == project_id
    assert updated_project["title"] == new_title
    
    print(f"✅ Проект обновлен: '{old_title}' → '{new_title}'")


def test_get_project_by_id(api_with_token):
    """Тест получения проекта по ID с проверкой статус-кода"""
    title = "Проект для получения по ID"
    
    # Создание проекта
    create_response = api_with_token.create_project(title)
    assert create_response.status_code == 201
    created_project = create_response.json()
    project_id = created_project["id"]
    
    # Получение проекта
    get_response = api_with_token.get_project_by_id(project_id)
    
    # Проверка статус-кода
    assert get_response.status_code == 200, f"Ожидался статус 200, получен {get_response.status_code}"
    
    # Проверка структуры ответа
    found_project = get_response.json()
    assert found_project is not None
    assert found_project["id"] == project_id
    assert found_project["title"] == title
    assert "companyId" in found_project
    assert "createdAt" in found_project
    assert "createdBy" in found_project
    assert "users" in found_project
    
    print(f"✅ Проект найден: '{found_project['title']}'")
