import pytest
import allure
from api_methods import register_user
from data.data import ALREADY_EXISTS_ERROR, REQUIRED_FIELDS_ERROR

@allure.epic("Авторизация")
@allure.feature("Регистрация пользователя")
class TestUserRegister:

    @allure.title("Успешная регистрация нового пользователя")
    def test_register_success(self, user_credentials):
        response = register_user(
            user_credentials["email"],
            user_credentials["password"],
            user_credentials["name"]
        )
        response_json = response.json()

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response_json["success"] is True, "Ожидался success=True"
        assert "user" in response_json, "Поле 'user' отсутствует в ответе"
        assert response_json["user"]["email"] == user_credentials["email"], "Email не совпадает"
        assert response_json["user"]["name"] == user_credentials["name"], "Имя не совпадает"
        assert "accessToken" in response_json, "Access token отсутствует в ответе"
        assert "refreshToken" in response_json, "Refresh token отсутствует в ответе"

    @allure.title("Регистрация существующего пользователя")
    def test_register_existing_user(self, registered_user):
        response = register_user(
            registered_user["email"],
            registered_user["password"],
            registered_user["name"]
        )
        response_json = response.json()

        assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        assert response_json["success"] is False, "Ожидался success=False"
        assert response_json["message"] == ALREADY_EXISTS_ERROR, "Неверное сообщение об ошибке"