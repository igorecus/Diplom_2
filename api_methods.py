import requests
import allure
from urls import *

@allure.step("Регистрация пользователя с email={email}, name={name}")
def register_user(email, password, name):
    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(REGISTER_URL, json=payload)
    return response

@allure.step("Авторизация пользователя с email={email}")
def login_user(email, password):
    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(LOGIN_URL, json=payload)
    return response

@allure.step("Получение данных пользователя")
def get_user(token):
    headers = {"authorization": token} if token else {}

    response = requests.get(USER_URL, headers=headers)
    return response

@allure.step("Обновление данных пользователя: {data}")
def update_user(token, data):
    headers = {"authorization": token} if token else {}

    response = requests.patch(USER_URL, headers=headers, json=data)
    return response

@allure.step("Выход пользователя из системы")
def logout_user(refresh_token):
    payload = {"token": refresh_token}

    response = requests.post(LOGOUT_URL, json=payload)
    return response

@allure.step("Создание заказа с ингредиентами: {ingredients}")
def create_order(ingredients, token=None):
    headers = {"authorization": token} if token else {}
    payload = {"ingredients": ingredients}

    response = requests.post(ORDERS_URL, headers=headers, json=payload)
    return response

@allure.step("Получение заказов пользователя")
def get_user_orders(token=None):
    headers = {"authorization": token} if token else {}

    response = requests.get(ORDERS_URL, headers=headers)
    return response

@allure.step("Получение всех заказов")
def get_all_orders():
    response = requests.get(ALL_ORDERS_URL)
    return response

@allure.step("Получение списка ингредиентов")
def get_ingredients():
    response = requests.get(INGREDIENTS_URL)
    return response