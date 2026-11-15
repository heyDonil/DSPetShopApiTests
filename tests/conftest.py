import random
import requests
import pytest

BASE_URL = 'https://petstore.swagger.rv-school.ru/api/v3'

@pytest.fixture()
def create_pet():
    pet_id = random.randint(1000,99999)
    payload = {
        "id": pet_id,
        "name": "Buddy",
        "status": "available"
    }

    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200, "Не удалось создать питомца в фикстуре"

    yield response.json()

    requests.delete(f"{BASE_URL}/pet/{pet_id}")
