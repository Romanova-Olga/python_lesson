import pytest
import requests

from api_YouGile_class import ProjectsAPI
from api_YouGile_class import AuthAPI
from api_YouGile_class import LOGIN, PASSWORD, COMPANY_ID, BASE_URL

def test_auth_success():
    """Тест успешной авторизации"""
    auth_api = AuthAPI(BASE_URL)
    response = auth_api.login(LOGIN, PASSWORD, COMPANY_ID)
    
    # Проверка статус-кода
    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
    
    # Проверка структуры ответа
    response_data = response.json()
    assert "key" in response_data, "Ответ не содержит поле 'key'"
    assert isinstance(response_data["key"], str), "Ключ должен быть строкой"
    assert len(response_data["key"]) > 0, "Ключ не должен быть пустым"
    
    print(f"✅ Токен получен: {response_data['key'][:20]}...")


def test_auth_invalid_password():
    """Тест авторизации с неверным паролем"""
    auth_api = AuthAPI(BASE_URL)
    response = auth_api.login(LOGIN, "wrong_password", COMPANY_ID)
    
    # Проверка, что авторизация не удалась
    assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"


def test_auth_invalid_login():
    """Тест авторизации с неверным логином"""
    auth_api = AuthAPI(BASE_URL)
    response = auth_api.login("wrong@email.com", PASSWORD, COMPANY_ID)
    
    assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"


def test_auth_invalid_company():
    """Тест авторизации с неверным ID компании"""
    auth_api = AuthAPI(BASE_URL)
    response = auth_api.login(LOGIN, PASSWORD, "invalid-company-id")
    
    assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"


def test_create_project(api_with_token):
    """Тест создания проекта с проверкой статус-кода"""
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


def test_create_project_without_title(api_with_token):
    """Тест создания проекта без заголовка (ожидается ошибка)"""
    response = api_with_token.create_project("")
    
    # Проверка, что сервер вернул ошибку
    assert response.status_code in [400, 422], f"Ожидался статус 400/422, получен {response.status_code}"


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


def test_update_nonexistent_project(api_with_token):
    """Тест обновления несуществующего проекта"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = api_with_token.update_project(fake_id, "Новый заголовок")
    
    # Проверка, что сервер вернул ошибку 404
    assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"


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


def test_get_nonexistent_project(api_with_token):
    """Тест получения несуществующего проекта"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = api_with_token.get_project_by_id(fake_id)
    
    # Проверка, что сервер вернул ошибку 404
    assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
