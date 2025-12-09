from fastapi.testclient import TestClient
from main import app, reset_database
import pytest


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tasks():
    """Reset tasks before each test"""
    reset_database()
    yield


def test_create_task():
    """Test creating a new task"""
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Task"
    assert data["description"] is None
    assert data["done"] is False
    assert "created_at" in data


def test_create_task_with_description():
    """Test creating a task with description"""
    response = client.post(
        "/tasks", 
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Test Description"


def test_list_tasks_empty():
    """Test listing tasks when there are none"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks():
    """Test listing multiple tasks"""
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_task():
    """Test getting a specific task"""
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"


def test_get_task_not_found():
    """Test getting a non-existent task"""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_title():
    """Test updating a task's title"""
    create_response = client.post("/tasks", json={"title": "Original Title"})
    task_id = create_response.json()["id"]
    
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_update_task_done():
    """Test marking a task as done"""
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    
    response = client.put(f"/tasks/{task_id}", json={"done": True})
    assert response.status_code == 200
    data = response.json()
    assert data["done"] is True


def test_update_task_not_found():
    """Test updating a non-existent task"""
    response = client.put("/tasks/999", json={"title": "New Title"})
    assert response.status_code == 404


def test_delete_task():
    """Test deleting a task"""
    create_response = client.post("/tasks", json={"title": "Task to Delete"})
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    """Test deleting a non-existent task"""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
