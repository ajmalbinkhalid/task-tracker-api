def get_token(client):

    client.post(
        "/auth/register",
        json={
            "username": "taskuser",
            "email": "task@example.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "task@example.com",
            "password": "123456"
        }
    )

    return response.json()["access_token"]


def test_create_task(client):

    token = get_token(client)

    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "Testing task creation"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_tasks(client):

    token = get_token(client)

    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200