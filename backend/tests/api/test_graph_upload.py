import io
import pytest

def test_upload_creates_project(client):
    data = {
        "files": (io.BytesIO(b"sample text content"), "sample.txt"),
        "simulation_requirement": "Predict how discussion evolves",
    }
    response = client.post(
        "/api/graph/ontology/generate",
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["project_id"].startswith("proj_")
