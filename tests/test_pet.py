import allure
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3'

@allure.feature('Pet')
class TestPet:
    @allure.title("Добавление нового питомца")
    def test_add_new_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
        with allure.step("Проверка статуса ответа и валидация JSON схемы"):
            assert response.status_code == 200
