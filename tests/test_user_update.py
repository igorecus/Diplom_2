import pytest
import allure
from api_methods import update_user
from data.data import AUTH_ERROR

@allure.epic("Управление пользователем")
@allure.feature("Редактирование данных пользователя")
class TestUserUpdate:

    @allure.title("Обновление имени авторизованного пользователя")
    def test_update_name_authorized(self, registered_user, faker):
        new_name = faker.name()

        response = update_user(
            registered_user["accessToken"],
            {"name": new_name}
        )
        response_json = response.json()

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response_json["success"] is True, "Ожидался success=True"
        assert response_json["user"]["name"] == new_name, "Имя не обновилось"

    @allure.title("Попытка обновления email авторизованного пользователя")
    def test_update_email_authorized(self, registered_user, faker):
        new_email = faker.email()

        response = update_user(
            registered_user["accessToken"],
            {"email": new_email}
        )
        response_json = response.json()

        assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        assert response_json["success"] is False, "Ожидался success=False"
        assert "message" in response_json, "Поле 'message' отсутствует в ответе"
        assert "email" in response_json["message"].lower(), "Сообщение об ошибке не содержит информацию о email"

    @allure.title("Обновление пароля авторизованного пользователя")
    def test_update_password_authorized(self, registered_user, faker):
        new_password = faker.password(length=12)

        response = update_user(
            registered_user["accessToken"],
            {"password": new_password}
        )
        response_json = response.json()

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response_json["success"] is True, "Ожидался success=True"

    @allure.title("Обновление имени неавторизованного пользователя")
    def test_update_name_unauthorized(self, faker):
        new_name = faker.name()

        response = update_user(
            None,
            {"name": new_name}
        )
        response_json = response.json()

        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response_json["success"] is False, "Ожидался success=False"
        assert response_json["message"] == AUTH_ERROR, "Неверное сообщение об ошибке"

    @allure.title("Обновление email неавторизованного пользователя")
    def test_update_email_unauthorized(self, faker):
        new_email = faker.email()

        response = update_user(
            None,
            {"email": new_email}
        )
        response_json = response.json()

        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response_json["success"] is False, "Ожидался success=False"
        assert response_json["message"] == AUTH_ERROR, "Неверное сообщение об ошибке"