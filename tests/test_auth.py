def test_register_and_login(client):
    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@example.com",
            "full_name": "Alice",
            "password": "Password123!",
        },
    )

    assert register.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "alice@example.com",
            "password": "Password123!",
        },
    )

    assert login.status_code == 200
    assert "access_token" in login.json()


def test_duplicate_email_is_rejected(client):
    payload = {
        "email": "alice@example.com",
        "full_name": "Alice",
        "password": "Password123!",
    }

    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409
