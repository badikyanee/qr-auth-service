def test_create_data(test_client):
    # 1. Регистрируем пользователя
    signup_response = test_client.post("/auth/signup", json={
        "username": "datauser123",
        "password": "testpass"
    })

    assert signup_response.status_code == 200

    # 2. Логинимся
    login_response = test_client.post("/auth/login", json={
        "username": "datauser123",
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

    assert response.status_code == 401