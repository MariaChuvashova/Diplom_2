import pytest
import allure
import requests
from urls import Url

class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, create_user):
        with allure.step("Отправляем POST-запрос на регистрацию уникального пользователя"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/register", json=create_user)
        with allure.step("Проверяем статус код"):
            assert response.status_code == 200
        with allure.step("Проверяем, что пользователь создан, и его данные"):
            data = response.json()
            assert data["success"] is True
            assert "user" in data


    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self):
        # Используем ваши реальные данные
        payload = {
            "email": "chuvashova_maria@mail.ru",
            "password": "password123",
            "name": "Мария"
        }
        with allure.step("Попытка повторной регистрации"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/register", json=payload)
        with allure.step("Проверяем ошибку 'User already exists'"):
            assert response.status_code == 403
            data = response.json()
            assert data['success'] is False
            assert data['message'] == 'User already exists'

    @allure.title("Создание пользователя без email")
    def test_create_user_without_email(self):
        payload = {
            "password": "password",
            "name": "Name"
        }
        with allure.step("Отправляем POST-запрос без email"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/register", json=payload)
        with allure.step("Проверяем, что сервер вернул ошибку"):
            assert response.status_code == 403
            data = response.json()
            assert data['success'] is False
            assert data['message'] == 'Email, password and name are required fields'


    @allure.title("Создание пользователя с пропущенным обязательным полем имя")
    def test_create_user_without_name(self):
        payload = {
            "email": "test-email@yandex.ru",
            "password": "password"
        }
        with allure.step("Отправляем POST-запрос без имени"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/register", json=payload)
        with allure.step("Проверяем, что сервер вернул ошибку"):
            assert response.status_code == 403
            data = response.json()
            assert data['success'] is False
            assert data['message'] == 'Email, password and name are required fields'


    @allure.title("Создание пользователя с пропущенным обязательным полем пароль")
    def test_create_user_without_password(self):
        payload = {
            "email": "test-email@yandex.ru",
            "name": "NAME"
        }
        with allure.step("Отправляем POST-запрос без пароля"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/register", json=payload)
        with allure.step("Проверяем, что сервер вернул ошибку"):
            assert response.status_code == 403
            data = response.json()
            assert data['success'] is False
            assert data['message'] == 'Email, password and name are required fields'
