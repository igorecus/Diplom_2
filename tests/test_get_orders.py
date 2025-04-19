import pytest
import allure
from api_methods import get_user_orders, create_order
from data.data import AUTH_ERROR

@allure.epic("Заказы")
@allure.feature("Получение заказов")
class TestGetOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_authorized(self, registered_user, ingredient_ids):
        if ingredient_ids:
            create_order([ingredient_ids[0]], registered_user["accessToken"])

        response = get_user_orders(registered_user["accessToken"])
        response_json = response.json()

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response_json["success"] is True, "Ожидался success=True"
        assert "orders" in response_json, "Поле 'orders' отсутствует в ответе"

        if ingredient_ids:
            assert len(response_json["orders"]) > 0, "Список заказов пуст"

    @allure.title("Невозможность получения заказов неавторизованного пользователя")
    def test_get_user_orders_unauthorized(self):
        response = get_user_orders()
        response_json = response.json()

        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response_json["success"] is False, "Ожидался success=False"
        assert response_json["message"] == AUTH_ERROR, "Неверное сообщение об ошибке"