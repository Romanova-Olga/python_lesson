import pytest
import requests

from YouGile_Api import ProjectsAPI


api = ProjectsAPI("https://ru.yougile.com")


# Проверка получения списка ключей
def test_get_keys(login = "romiolemarak@gmail.com", password = "_GSUb_3nD#Um76h"):
    login = "login"
    password = "password"
    result = api.get_keys_list(login, password)
    assert result


# Проверка создания проекта
def test_create_project():
    login = "login"
    password = "password"
    my_token = api.get_keys_list(login, password)
    title = "Старый проект"
    result = api.create_project(title)
    new_id = result.json().get("id")
    new_project = api.create_project("new_id")
    assert new_project.status_code == 200
    assert new_project.json()["id"] == new_id


# Провека изменения проекта
def test_update_project():
    login = "login"
    password = "password"
    my_token = api.get_keys_list(login, password)
    new_title = "Новый проект"
    result = api.update_project(new_title)
    assert result


# Проверка получения проекта по ID
def test_get_project_id():
    login = "login"
    password = "password"
    my_token = api.get_keys_list(login, password)
    found_project = api.get_project_id(id)
    assert found_project
