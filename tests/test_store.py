import allure
import jsonschema
import requests
from .schemas.store_schema import STORE_SCHEMA, ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:

    @allure.title("Размещение заказа")
    def test_placing_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_json["id"] == payload["id"], "id заказа не совпал с ожидаемым"
            assert response_json["petId"] == payload["petId"], "petId заказа не совпал с ожидаемым"
            assert response_json["quantity"] == payload["quantity"], "quantity заказа не совпал с ожидаемым"
            assert response_json["status"] == payload["status"], "status заказа не совпал с ожидаемым"
            assert response_json["complete"] == payload["complete"], "complete заказа не совпал с ожидаемым"
            jsonschema.validate(response.json(), ORDER_SCHEMA)

    @allure.title("Получение информации о заказе по ID")
    def test_get_info_of_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка соответствия ID заказа"):
            assert response.json()["id"] == order_id, "ID заказа не совпал с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса проверки удаления заказа"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
            assert response.text == "Order not found", "Тело ответа не совпало с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_info_of_nonexistent_order(self):
        with allure.step("Попытка получить информацию о несуществующем заказе"):
            response = requests.get(f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
            assert response.text == "Order not found", "Содержимое ответа не совпадает с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение инвенторя"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json(), STORE_SCHEMA)