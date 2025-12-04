import allure
import requests
from urls import Url


class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, registered_user, login_user):
        # Получаем список ингредиентов
        ingredients_response = requests.get(f"{Url.BASE_URL}/api/ingredients")
        ingredients_data = ingredients_response.json()["data"]
        
        # Берём первые два ингредиента
        ingredients = [ingredients_data[0]["_id"], ingredients_data[1]["_id"]]
        
        headers = {"Authorization": login_user}
        payload = {"ingredients": ingredients}
        
        with allure.step("Создаём заказ с авторизацией"):
            response = requests.post(f"{Url.BASE_URL}/api/orders", json=payload, headers=headers)
        
        with allure.step("Проверяем успешное создание заказа"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "order" in data
            assert "number" in data["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        # Получаем список ингредиентов
        ingredients_response = requests.get(f"{Url.BASE_URL}/api/ingredients")
        ingredients_data = ingredients_response.json()["data"]
        
        ingredients = [ingredients_data[0]["_id"]]
        payload = {"ingredients": ingredients}
        
        with allure.step("Создаём заказ без авторизации"):
            response = requests.post(f"{Url.BASE_URL}/api/orders", json=payload)
        
        with allure.step("Проверяем, что заказ создаётся (API разрешает)"):
            # API возвращает 200 даже без авторизации
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "name" in data
            assert "order" in data
            assert "number" in data["order"]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user, login_user):
        headers = {"Authorization": login_user}
        payload = {"ingredients": []}
        
        with allure.step("Создаём заказ без ингредиентов"):
            response = requests.post(f"{Url.BASE_URL}/api/orders", json=payload, headers=headers)
        
        with allure.step("Проверяем ошибку"):
            assert response.status_code == 400
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash(self, registered_user, login_user):
        headers = {"Authorization": login_user}
        payload = {"ingredients": ["invalid_hash_1", "invalid_hash_2"]}
        
        with allure.step("Создаём заказ с неверными хешами"):
            response = requests.post(f"{Url.BASE_URL}/api/orders", json=payload, headers=headers)
        
        with allure.step("Проверяем ошибку сервера"):
            assert response.status_code == 500
