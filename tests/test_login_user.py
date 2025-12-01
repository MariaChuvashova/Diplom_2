import allure
import requests
from urls import Url


class TestLoginUser:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        with allure.step("Отправляем POST-запрос на авторизацию"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/login", json=payload)
        with allure.step("Проверяем успешную авторизацию"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "accessToken" in data
            assert "refreshToken" in data
            assert "user" in data

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": "wrong_password"
        }
        with allure.step("Отправляем POST-запрос с неверным паролем"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/login", json=payload)
        with allure.step("Проверяем ошибку авторизации"):
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "email or password are incorrect"

    @allure.title("Логин с неверным email")
    def test_login_wrong_email(self):
        payload = {
            "email": "nonexistent@test.com",
            "password": "password123"
        }
        with allure.step("Отправляем POST-запрос с неверным email"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/login", json=payload)
        with allure.step("Проверяем ошибку авторизации"):
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "email or password are incorrect"

    @allure.title("Логин без заполнения одного из полей")
    def test_login_without_field(self):
        payload = {
            "email": "test@test.com"
        }
        with allure.step("Отправляем POST-запрос без пароля"):
            response = requests.post(f"{Url.BASE_URL}/api/auth/login", json=payload)
        with allure.step("Проверяем ошибку"):
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "email or password are incorrect"
