import io
import pytest

def test_upload_creates_project(client):
    files = {"files": ("sample.txt", io.BytesIO(b"sample text content"))}
    data = {"simulation_requirement": "Predict how discussion evolves"}
    response = client.post(
        "/api/graph/ontology/generate",
        data=data,
        files=files,
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["project_id"].startswith("proj_")
