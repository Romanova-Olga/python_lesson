import requests


class ProjectsAPI:

    # Инициализация
    def __init__(self, url) -> None:
        self.url = url

    # Получение списка ключей
    def get_keys_list(self, login, password):
        body = {
            "login" : login,
            "password" : password
        }
        resp = requests.post(self.url + '/api-v2/auth/keys/get', json=body)
        return resp.json()["key"]

    # Создание проект
    def create_project(self, title):
        my_token = self.get_keys_list()
        my_headers = {
            "Content-Type" : "application/json",
            "Authorization" : "Bearer " + my_token
        }
        project = {
            "title": title
        }
        resp = requests.post(self.url + '/api-v2/projects', json=project,
                             headers=my_headers)
        return resp.json()["id"]

    # Изменение проекта
    def update_project(self, id, new_title):
        my_token = self.get_keys_list()
        my_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + my_token
        }
        new_project = {
            "title": new_title
        }
        resp = requests.put(self.url + f'/api-v2/projects/{id}',
                            json=new_project, headers=my_headers)
        return resp.json()["id"]

    # Получение проекта по ID
    def get_project_id(self, id):
        my_token = self.get_keys_list()
        my_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + my_token
        }
        resp = requests.get(self.url + f'/api-v2/projects/{id}',
                            headers=my_headers)
        return resp.json
    