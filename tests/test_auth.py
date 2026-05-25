import uuid


def test_signup(test_client):
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    response = test_client.post("/auth/signup", json={
        "username": unique_username,
        "password": "testpass"
    })

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == unique_username
    assert "id" in data


def test_login(test_client):
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    test_client.post("/auth/signup", json={
        "username": unique_username,
        "password": "testpass"
    })

    response = test_client.post("/auth/login", json={
        "username": unique_username,
        "password": "testpass"
    })

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"