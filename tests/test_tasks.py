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
