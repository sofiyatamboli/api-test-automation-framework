"""
Automated API test suite for the Task Manager API.
Run with: pytest -v
Run with HTML report: pytest -v --html=report.html --self-contained-html
"""

import pytest
from app import create_app
from models import db, Task


@pytest.fixture
def client():
    """Creates a fresh Flask app bound to an isolated in-memory SQLite
    database for each test, so tests don't depend on execution order
    or leak state into one another."""
    test_app = create_app(db_uri="sqlite:///:memory:")
    test_app.config["TESTING"] = True

    with test_app.test_client() as client:
        yield client

    with test_app.app_context():
        db.session.remove()
        db.drop_all()


# ---------- Health check ----------

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


# ---------- GET /tasks ----------

def test_get_all_tasks_returns_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_single_task_success(client):
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert "title" in data
    assert "completed" in data


def test_get_single_task_not_found(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert "error" in response.get_json()


# ---------- POST /tasks ----------

def test_create_task_success(client):
    response = client.post("/tasks", json={"title": "Write documentation"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Write documentation"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_missing_title_returns_400(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_task_empty_title_returns_400(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400


def test_create_task_no_body_returns_400(client):
    response = client.post("/tasks")
    assert response.status_code == 400


# ---------- PUT /tasks/<id> ----------

def test_update_task_title(client):
    response = client.put("/tasks/1", json={"title": "Updated title"})
    assert response.status_code == 200
    assert response.get_json()["title"] == "Updated title"


def test_update_task_completed_status(client):
    response = client.put("/tasks/1", json={"completed": True})
    assert response.status_code == 200
    assert response.get_json()["completed"] is True


def test_update_nonexistent_task_returns_404(client):
    response = client.put("/tasks/9999", json={"title": "Nope"})
    assert response.status_code == 404


def test_update_task_empty_title_returns_400(client):
    response = client.put("/tasks/1", json={"title": "   "})
    assert response.status_code == 400
    assert "error" in response.get_json()


# ---------- DELETE /tasks/<id> ----------

def test_delete_task_success(client):
    created = client.post("/tasks", json={"title": "Temp task"}).get_json()
    task_id = created["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    follow_up = client.get(f"/tasks/{task_id}")
    assert follow_up.status_code == 404


def test_delete_nonexistent_task_returns_404(client):
    response = client.delete("/tasks/9999")
    assert response.status_code == 404