# Product service tests

import pytest
from app.app import app
import requests

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
    assert data["service"] == "product-service"


def test_get_product_found(client):
    response = client.get("/product/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1200


def test_get_product_not_found(client):
    response = client.get("/product/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_get_product_with_user_success(monkeypatch, client):
    """Teste la récupération d’un produit avec un utilisateur (mock du user-service)"""
    def mock_get(url, timeout):
        class MockResponse:
            status_code = 200
            def json(self):
                return {"id": 1, "name": "John Doe"}
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get("/product/1/user")
    assert response.status_code == 200
    data = response.get_json()
    assert "product" in data
    assert "owner" in data
    assert data["owner"]["name"] == "John Doe"


def test_get_product_with_user_unreachable(monkeypatch, client):
    """Teste l’erreur quand le user-service ne répond pas"""
    def mock_get(url, timeout):
        raise requests.exceptions.ConnectionError("user-service unreachable")

    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get("/product/1/user")
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Failed to contact user-service"

