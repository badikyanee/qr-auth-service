import uuid

def test_create_data(test_client):
    # Генерируем уникальное имя пользователя, чтобы тесты не падали при повторном запуске
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    # 1. Регистрируем пользователя
    signup_response = test_client.post("/auth/signup", json={
        "username": unique_username,
        "password": "testpass"
    })

    assert signup_response.status_code == 200

    # 2. Логинимся
    # ИСПРАВЛЕНО: передаем данные через data= (как форму form-data) и используем unique_username
    login_response = test_client.post("/auth/login", data={
        "username": unique_username,
        "password": "testpass"
    })

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # 3. Отправляем защищённый запрос
    response = test_client.post(
        "/data/",
        json={"text": "secret data"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["text"] == "secret data"
    assert "id" in data


def test_create_data_without_token(test_client):
    response = test_client.post(
        "/data/",
        json={"text": "secret data"}
    )

    # Проверяем, что кастомное AuthMiddleware успешно блокирует запросы без токена
    assert response.status_code == 401
