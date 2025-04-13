import pytest
import allure
from faker import Faker
from api_methods import register_user, login_user, logout_user, get_ingredients
from helpers import random_email, random_name, random_password
from data.data import DEFAULT_PASSWORD

fake = Faker(['ru_RU'])

@pytest.fixture
def faker():
    return fake

@pytest.fixture
def user_credentials(faker):
    credentials = {
        "email": faker.email(),
        "password": DEFAULT_PASSWORD,
        "name": faker.name()
    }

    allure.attach(
        f"Email: {credentials['email']}\nName: {credentials['name']}",
        name="Учетные данные пользователя",
        attachment_type=allure.attachment_type.TEXT
    )

    return credentials

@pytest.fixture
def registered_user(user_credentials):
    # Регистрация пользователя
    response = register_user(
        user_credentials["email"],
        user_credentials["password"],
        user_credentials["name"]
    )

    response_json = response.json()

    access_token = response_json.get("accessToken")
    refresh_token = response_json.get("refreshToken")

    user_data = {
        "email": user_credentials["email"],
        "password": user_credentials["password"],
        "name": user_credentials["name"],
        "accessToken": access_token,
        "refreshToken": refresh_token
    }

    yield user_data

    if refresh_token:
        logout_user(refresh_token)


@pytest.fixture
def ingredient_ids():
    response = get_ingredients()

    ingredient_ids = []
    if response.status_code == 200:
        data = response.json().get('data', [])
        ingredient_ids = [item.get('_id') for item in data if '_id' in item]

    return ingredient_ids