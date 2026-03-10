import pytest
from core import create_app

from fastapi.testclient import TestClient

@pytest.fixture
def client():
    app = create_app()
    client = TestClient(app)
    yield client

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
