def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_login_user(client):
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()