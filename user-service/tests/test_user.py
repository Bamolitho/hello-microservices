import pytest
from app.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "user-service"


def test_get_user_found(client):
    response = client.get("/user/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Alice"


def test_get_user_not_found(client):
    response = client.get("/user/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
