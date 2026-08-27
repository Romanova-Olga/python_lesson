import requests
import pytest


class AuthAPI:
    """Класс для работы с API авторизации"""
    
    def __init__(self, url):
        self.url = url
    
    def login(self, login, password, company_id):
        """Авторизация и получение токена"""
        auth_data = {
            "login": login,
            "password": password,
            "companyId": company_id
        }
        
        resp = requests.post(
            self.url + "/api-v2/auth/login",
            json=auth_data
        )
        
        return resp


class ProjectsAPI:
    """Класс для работы с проектами"""

    def __init__(self, url, token=None) -> None:
        self.url = url
        self.token = token

    def set_token(self, token):
        """Установка токена"""
        self.token = token

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }

    def create_project(self, title):
        project = {
            "title": title
        }

        resp = requests.post(
            self.url + "/api-v2/projects",
            json=project,
            headers=self.get_headers()
        )

        return resp

    def update_project(self, project_id, new_title):
        new_project = {
            "title": new_title
        }

        resp = requests.put(
            self.url + f"/api-v2/projects/{project_id}",
            json=new_project,
            headers=self.get_headers()
        )

        return resp

    def get_project_by_id(self, project_id):
        resp = requests.get(
            self.url + f"/api-v2/projects/{project_id}",
            headers=self.get_headers()
        )

        return resp


# Данные для авторизации
LOGIN = "romiolemarak@gmail.com"
PASSWORD = "KaramelLublu"
COMPANY_ID = "e6bcfea7-6256-4085-85de-47405e2c0147"
BASE_URL = "https://ru.yougile.com"


@pytest.fixture
def auth_token():
    """Фикстура для получения токена"""
    auth_api = AuthAPI(BASE_URL)
    response = auth_api.login(LOGIN, PASSWORD, COMPANY_ID)
    
    assert response.status_code == 201, f"Ошибка авторизации: {response.status_code}"
    
    response_data = response.json()
    assert "key" in response_data, "В ответе отсутствует ключ"
    assert response_data["key"] is not None, "Ключ пустой"
    
    return response_data["key"]


@pytest.fixture
def api_with_token(auth_token):
    """Фикстура с авторизованным API"""
    return ProjectsAPI(BASE_URL, auth_token)
