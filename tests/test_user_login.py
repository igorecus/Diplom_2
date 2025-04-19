import pytest
import allure
from api_methods import login_user, register_user
from data.data import INVALID_CREDENTIALS_ERROR

@allure.epic("Авторизация")
@allure.feature("Вход пользователя")
class TestUserLogin:

    @allure.title("Успешная авторизация существующего пользователя")
    def test_login_success(self, registered_user):
        response = login_user(
            registered_user["email"],
            registered_user["password"]
        )
        response_json = response.json()

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response_json["success"] is True, "Ожидался success=True"

        assert "user" in response_json, "Поле 'user' отсутствует в ответе"
        assert response_json["user"]["email"] == registered_user["email"], "Email не совпадает"
        assert response_json["user"]["name"] == registered_user["name"], "Имя не совпадает"

        assert "accessToken" in response_json, "Access token отсутствует в ответе"
        assert "refreshToken" in response_json, "Refresh token отсутствует в ответе"

    @allure.title("Авторизация с неверным паролем")
    def test_login_wrong_password(self, registered_user):
        response = login_user(
            registered_user["email"],
            "wrong_password"
        )
        response_json = response.json()

        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response_json["success"] is False, "Ожидался success=False"
        assert response_json["message"] == INVALID_CREDENTIALS_ERROR, "Неверное сообщение об ошибке"

    @allure.title("Авторизация с неверным email")
    def test_login_wrong_email(self, registered_user):
        response = login_user(
            "wrong_" + registered_user["email"],
            registered_user["password"]
        )
        response_json = response.json()

        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response_json["success"] is False, "Ожидался success=False"
        assert response_json["message"] == INVALID_CREDENTIALS_ERROR, "Неверное сообщение об ошибке"