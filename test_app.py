import pytest

from app import app, tasks


@pytest.fixture
def client():
    app.config["TESTING"] = True
    tasks.clear()

    with app.test_client() as client:
        yield client

    tasks.clear()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_create_and_list_task(client):
    response = client.post("/tasks", json={"title": "Learn Docker"})

    assert response.status_code == 201
    task = response.get_json()
    assert task == {
        "id": 1,
        "title": "Learn Docker",
        "completed": False,
    }

    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == [task]


def test_reject_empty_title(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 400
    assert response.get_json() == {
        "error": "A task title is required"
    }


def test_reject_invalid_body(client):
    response = client.post("/tasks", json=[])
    assert response.status_code == 400
    assert response.get_json() == {"error": "Send a JSON object"}

