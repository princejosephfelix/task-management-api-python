def test_create_and_get_task(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    create = client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Learn REST APIs",
            "description": "Compare FastAPI, Spring Boot and ASP.NET Core",
            "priority": "HIGH",
        },
    )

    assert create.status_code == 201
    task = create.json()
    assert task["title"] == "Learn REST APIs"
    assert task["priority"] == "HIGH"

    get_response = client.get(
        f"/api/v1/tasks/{task['id']}",
        headers=headers,
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task["id"]


def test_list_tasks_with_search(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    client.post(
        "/api/v1/tasks",
        headers=headers,
        json={"title": "Docker practice"},
    )
    client.post(
        "/api/v1/tasks",
        headers=headers,
        json={"title": "Kubernetes practice"},
    )

    response = client.get(
        "/api/v1/tasks?search=Docker&page=1&page_size=10",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_unauthenticated_task_access_is_rejected(client):
    response = client.get("/api/v1/tasks")
    assert response.status_code in (401, 403)

def test_get_nonexistent_task_returns_404(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    response = client.get(
        "/api/v1/tasks/999999",
        headers=headers,
    )

    assert response.status_code == 404
    
def test_user_cannot_access_another_users_task(client, user_token):
    owner_headers = {"Authorization": f"Bearer {user_token}"}

    create = client.post(
        "/api/v1/tasks",
        headers=owner_headers,
        json={"title": "Private task"},
    )

    assert create.status_code == 201
    task_id = create.json()["id"]

    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": "bob@example.com",
            "full_name": "Bob",
            "password": "Password123!",
        },
    )

    assert register.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "bob@example.com",
            "password": "Password123!",
        },
    )

    assert login.status_code == 200

    bob_token = login.json()["access_token"]
    bob_headers = {"Authorization": f"Bearer {bob_token}"}

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=bob_headers,
    )

    assert response.status_code == 403
    
    
def test_update_task(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    create = client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": "Original title",
            "description": "Original description",
        },
    )

    assert create.status_code == 201
    task_id = create.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={
            "title": "Updated title",
            "description": "Updated description",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["description"] == "Updated description"
    
def test_delete_task(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    create = client.post(
        "/api/v1/tasks",
        headers=headers,
        json={"title": "Task to delete"},
    )

    assert create.status_code == 201
    task_id = create.json()["id"]

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert get_response.status_code == 404
    
    