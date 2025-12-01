import pytest
import requests
from helpers import generate_email, generate_password, generate_name
from urls import Url


@pytest.fixture
def create_user():
    """Фикстура генерации данных пользователя (без создания на сервере)"""
    email = generate_email()
    password = generate_password()
    name = generate_name()
    return {
        "email": email,
        "password": password,
        "name": name
    }


@pytest.fixture
def registered_user():
    """Фикстура создания зарегистрированного пользователя"""
    email = generate_email()
    password = generate_password()
    name = generate_name()
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(f"{Url.BASE_URL}/api/auth/register", json=payload)
    response.raise_for_status()
    return payload


@pytest.fixture
def login_user(registered_user):
    """Фикстура получения токена авторизации"""
    response = requests.post(f"{Url.BASE_URL}/api/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    response.raise_for_status()
    return response.json().get("accessToken")
