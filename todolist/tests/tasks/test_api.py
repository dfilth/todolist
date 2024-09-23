import pytest
from rest_framework import status
from rest_framework.test import APIClient
from todolist.tasks.models import Task


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def sample_task():
    return Task.objects.create(
        title="Sample Task", description="Sample Description", completed=False
    )


def perform_request(client, method, url, data=None):
    response = getattr(client, method)(url, data, format="json")
    return response


@pytest.mark.django_db
def test_get_tasks(client, sample_task):
    response = perform_request(client, "get", "/tasks/")
    assert response.status_code == 200
    assert len(response.data) > 0


@pytest.mark.django_db
def test_post_task(client):
    task = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
    }
    response = perform_request(client, "post", "/tasks/", task)
    assert response.status_code == 201
    assert response.data["task"]["id"] == 1


@pytest.mark.django_db
def test_update_task(client, sample_task):
    updated_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True,
    }
    response = perform_request(
        client, "put", f"/tasks/{sample_task.id}/", updated_data
    )
    assert response.status_code == 200
    assert response.data["task"]["title"] == "Updated Task"
    assert response.data["task"]["completed"] is True


@pytest.mark.django_db
def test_delete_task(client, sample_task):
    response = perform_request(client, "delete", f"/tasks/{sample_task.id}/")
    assert response.status_code == 204

    response = perform_request(client, "get", f"/tasks/{sample_task.id}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_task_with_invalid_boolean(client):
    task_invalid = {
        "title": "Invalid Task",
        "description": "This task has an invalid completed field",
        "completed": "not_a_boolean",
    }
    response = perform_request(client, "post", "/tasks/", task_invalid)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "completed" in response.data["errors"]
    assert response.data["errors"]["completed"] == ["Must be a valid boolean."]


@pytest.mark.django_db
def test_crud_tasks_integration(client):
    # 1. Create task
    task_data = {
        "title": "Integration Task",
        "description": "Integration Description",
        "completed": False,
    }
    response = client.post("/tasks/", task_data, format="json")
    assert response.status_code == 201
    created_task_id = response.data["task"]["id"]

    # 2. Get created task
    response = client.get(f"/tasks/{created_task_id}/")
    assert response.status_code == 200
    assert response.data["task"]["title"] == "Integration Task"

    # 3. Update task
    updated_data = {
        "title": "Updated Integration Task",
        "description": "Updated Description",
        "completed": True,
    }
    response = client.put(
        f"/tasks/{created_task_id}/", updated_data, format="json"
    )
    assert response.status_code == 200
    assert response.data["task"]["title"] == "Updated Integration Task"
    assert response.data["task"]["completed"] is True

    # 4. Delete Task
    response = client.delete(f"/tasks/{created_task_id}/")
    assert response.status_code == 204

    # 5. Verify deleted task
    response = client.get(f"/tasks/{created_task_id}/")
    assert response.status_code == 404
