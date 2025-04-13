import pytest
import allure
from api_methods import create_order
from data.data import NO_INGREDIENTS_ERROR

@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа авторизованным пользователем с ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, registered_user, ingredient_ids):
        ingredients = ingredient_ids[:2] if len(ingredient_ids) >= 2 else ingredient_ids

        response = create_order(
            ingredients,
            registered_user["accessToken"]
        )
        response_json = response.json()

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response_json["success"] is True, "Ожидался success=True"
        assert "order" in response_json, "Поле 'order' отсутствует в ответе"
        assert "number" in response_json["order"], "Поле 'number' отсутствует в ответе"

    @allure.title("Создание заказа неавторизованным пользователем с ингредиентами")
    def test_create_order_without_auth_with_ingredients(self, ingredient_ids):
        ingredients = ingredient_ids[:2] if len(ingredient_ids) >= 2 else ingredient_ids

        response = create_order(ingredients)
        response_json = response.json()

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response_json["success"] is True, "Ожидался success=True"
        assert "order" in response_json, "Поле 'order' отсутствует в ответе"
        assert "number" in response_json["order"], "Поле 'number' отсутствует в ответе"

    @allure.title("Невозможность создания заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user):
        response = create_order(
            [],
            registered_user["accessToken"]
        )
        response_json = response.json()

        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
        assert response_json["success"] is False, "Ожидался success=False"
        assert response_json["message"] == NO_INGREDIENTS_ERROR, "Неверное сообщение об ошибке"

    @allure.title("Невозможность создания заказа с неверным ID ингредиента")
    def test_create_order_invalid_ingredient(self, registered_user):
        response = create_order(
            ["invalid_ingredient_id"],
            registered_user["accessToken"]
        )

        assert response.status_code == 500, f"Ожидался код 500, получен {response.status_code}"