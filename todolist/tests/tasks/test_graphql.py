import pytest
from todolist.tasks.models import Task
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def task():
    return Task.objects.create(
        title="Original Task",
        description="Original Description",
        completed=False,
    )


def execute_graphql(client, query, variables=None):
    response = client.post(
        "/graphql/", {"query": query, "variables": variables}, format="json"
    )
    return response.json(), response.status_code


@pytest.mark.django_db
def test_create_task_graphql(client):
    mutation = """
    mutation ($title: String!, $description: String!, $completed: Boolean!) {
        createTask(title: $title, description: $description, completed: $completed) {
            id
            title
            description
            completed
        }
    }
    """
    variables = {
        "title": "New Task",
        "description": "Task Description",
        "completed": False,
    }

    data, status_code = execute_graphql(client, mutation, variables)
    task_data = data["data"]["createTask"]

    assert status_code == 200
    assert task_data["title"] == "New Task"
    assert task_data["completed"] is False


@pytest.mark.django_db
def test_get_task_graphql(client, task):
    query = """
    query ($id: Int!) {
        taskById(id: $id) {
            id
            title
            description
            completed
        }
    }
    """
    variables = {"id": task.id}

    data, status_code = execute_graphql(client, query, variables)
    task_data = data["data"]["taskById"]

    assert status_code == 200
    assert task_data["title"] == "Original Task"
    assert task_data["description"] == "Original Description"
    assert task_data["completed"] is False


@pytest.mark.django_db
def test_update_task_graphql(client, task):
    mutation = """
    mutation updateTask($id: Int!, $title: String, $description: String, $completed: Boolean) {
        updateTask(id: $id, title: $title, description: $description, completed: $completed) {
            id
            title
            description
            completed
        }
    }
    """
    variables = {
        "id": task.id,
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True,
    }

    data, status_code = execute_graphql(client, mutation, variables)
    task_data = data["data"]["updateTask"]

    assert status_code == 200
    assert task_data["title"] == "Updated Task"
    assert task_data["completed"] is True


@pytest.mark.django_db
def test_delete_task_graphql(client, task):
    mutation = """
    mutation ($id: Int!) {
        deleteTask(id: $id)
    }
    """
    variables = {"id": task.id}

    data, status_code = execute_graphql(client, mutation, variables)
    assert status_code == 200
    assert data["data"]["deleteTask"] is True

    query = "{ taskById(id: %d) { id } }" % task.id
    data, status_code = execute_graphql(client, query)
    assert data["data"] is None


@pytest.mark.django_db
def test_crud_tasks_graphql(client):
    # 1. Create task
    mutation_create = """
    mutation ($title: String!, $description: String!, $completed: Boolean!) {
        createTask(title: $title, description: $description, completed: $completed) {
            id
            title
            description
            completed
        }
    }
    """
    variables_create = {
        "title": "Integration Task",
        "description": "Integration Description",
        "completed": False,
    }
    response = client.post(
        "/graphql/",
        {"query": mutation_create, "variables": variables_create},
        format="json",
    )
    assert response.status_code == 200
    created_task_id = response.json()["data"]["createTask"]["id"]

    # 2. Get created task
    query_get = """
    query ($id: Int!) {
        taskById(id: $id) {
            id
            title
            description
            completed
        }
    }
    """
    variables_get = {
        "id": created_task_id,
    }
    response = client.post(
        "/graphql/",
        {"query": query_get, "variables": variables_get},
        format="json",
    )
    data = response.json()["data"]["taskById"]
    assert response.status_code == 200
    assert data["title"] == "Integration Task"

    # 3. Update task
    mutation_update = """
    mutation ($id: Int!, $title: String!, $description: String!, $completed: Boolean!) {
        updateTask(id: $id, title: $title, description: $description, completed: $completed) {
            id
            title
            description
            completed
        }
    }
    """
    variables_update = {
        "id": created_task_id,
        "title": "Updated Integration Task",
        "description": "Updated Description",
        "completed": True,
    }
    response = client.post(
        "/graphql/",
        {"query": mutation_update, "variables": variables_update},
        format="json",
    )
    data = response.json()["data"]["updateTask"]
    assert response.status_code == 200
    assert data["title"] == "Updated Integration Task"
    assert data["completed"] is True

    # 4. Delete Task
    mutation_delete = """
    mutation ($id: Int!) {
        deleteTask(id: $id)
    }
    """
    variables_delete = {
        "id": created_task_id,
    }
    response = client.post(
        "/graphql/",
        {"query": mutation_delete, "variables": variables_delete},
        format="json",
    )
    assert response.status_code == 200
    assert response.json()["data"]["deleteTask"] is True

    # 5. Verify deleted task
    response = client.post(
        "/graphql/",
        {"query": "{ taskById(id: %d) { id } }" % created_task_id},
        format="json",
    )
    data = response.json()["data"]
    assert data is None
