from urllib import response

import allure
import requests
from tests.schemas.pet_schema import PET_SCHEMA
import jsonschema

BASE_URL = 'https://petstore.swagger.rv-school.ru/api/v3'


@allure.feature('Pet')
class TestPet:

    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == 'Pet deleted', 'Текст ответа не совпал с ожидаемым'

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999, "name": "Non-existent Pet", "status": "available"}
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == 'Pet not found', 'Текст ответа не совпал с ожидаемым'

    @allure.title("Добавление нового питомца с минимальным набором полей")
    def test_add_pet_min_fields(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "photoUrls": ["url"],
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], 'id не совпадает с ожидаемым'
            assert response_json['name'] == payload['name'], 'name не совпадает с ожидаемым'
            assert response_json['photoUrls'] == payload['photoUrls'], 'photoUrls не совпадает с ожидаемым'
            assert response_json['status'] == payload['status'], 'status не совпадает с ожидаемым'


    @allure.title("Добавление питомца со всеми полями")
    def test_add_pet_all_fields(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 5,
                "name": 'Pavel',
                "category": {
                    "id": 1,
                    "name": 'Cats'
                },
                "photoUrls": ['some/urls'],
                "tags": [{
                    "id": 2,
                    "name": 'tag',
                }],
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса и тела ответа"):
            assert response.status_code == 200
            assert response_json['id'] == payload['id']
            assert response_json['name'] == payload['name']
            assert response_json['category'] == payload['category']
            assert response_json['photoUrls'] == payload['photoUrls']
            assert response_json['tags'] == payload['tags']
            assert response_json['status'] == payload['status']

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']
        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()['id'] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet_info(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']
        with allure.step("Подготовка данных для обновления питомца"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }
        with allure.step("Отправка запроса на обновление питомца"):
            response = requests.put(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса и тела ответа"):
            assert response.status_code == 200
            assert response_json['id'] == payload['id']
            assert response_json['name'] == payload['name']
            assert response_json['status'] == payload['status']

    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']
        with allure.step("Отправление запроса на удаление питомца"):
            r1 = requests.delete(f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа"):
            assert r1.status_code == 200
        with allure.step("Отправка запроса на получение питомца"):
            r2 = requests.get(f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа"):
            assert r2.status_code == 404
