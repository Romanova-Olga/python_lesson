import pytest
import requests

from YouGile_Api import ProjectsAPI


api = ProjectsAPI("https://ru.yougile.com")


# Проверка получения списка ключей
def test_get_keys(login="romiolemarak@gmail.com", password="_GSUb_3nD#Um76h"):
    result = api.get_keys_list(login, password)
    assert result


# Проверка создания проекта
def test_create_project():
    login = "login"
    password = "password"
    my_token = api.get_keys_list(login, password)
    title = "Старый проект"
    result = api.create_project(title, my_token)
    new_id = result
    
    # Создаем новый проект с тем же ID для проверки
    new_project = api.create_project("Новый проект", my_token)
    assert new_project is not None
    assert new_project != new_id


# Провека изменения проекта
def test_update_project():
    login = "login"
    password = "password"
    my_token = api.get_keys_list(login, password)
    new_title = "Новый проект"
    result = api.update_project(new_title, my_token)
    assert result


# Проверка получения проекта по ID
def test_get_project_id():
    login = "login"
    password = "password"
    my_token = api.get_keys_list(login, password)
    project_id = "some_project_id"
    found_project = api.get_project_id(project_id, my_token)
    assert found_project 
