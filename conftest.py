import pytest
import allure
from faker import Faker
from api_methods import register_user, logout_user, get_ingredients
from data.data import DEFAULT_PASSWORD

fake = Faker(['ru_RU'])


@pytest.fixture
def registered_user():
    credentials = {
        "email": fake.email(),
        "password": DEFAULT_PASSWORD,
        "name": fake.name()
    }

    allure.attach(
        f"Email: {credentials['email']}\nName: {credentials['name']}",
        name="Учетные данные пользователя",
        attachment_type=allure.attachment_type.TEXT
    )

    response = register_user(
        credentials["email"],
        credentials["password"],
        credentials["name"]
    )

    response_json = response.json()

    access_token = response_json.get("accessToken")
    refresh_token = response_json.get("refreshToken")

    user_data = {
        "email": credentials["email"],
        "password": credentials["password"],
        "name": credentials["name"],
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