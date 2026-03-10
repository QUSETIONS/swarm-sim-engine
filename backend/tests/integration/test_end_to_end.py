import io
import pytest

def test_end_to_end_pipeline(client):
    data = {
        "files": (io.BytesIO(b"sample text content"), "sample.txt"),
        "simulation_requirement": "Predict discussion",
    }
    res1 = client.post("/api/graph/ontology/generate", data=data, content_type="multipart/form-data")
    assert res1.status_code == 200
    project_id = res1.json["data"]["project_id"]
    
    res2 = client.post("/api/graph/build", json={"project_id": project_id})
    assert res2.status_code == 200
    
    res3 = client.post("/api/simulation/profiles/generate", json={"entities": [{"name": "A"}, {"name": "B"}]})
    assert res3.status_code == 200
    
    res4 = client.post("/api/simulation/config/generate", json={"project_id": project_id, "entities": [{"name":"A"}]})
    assert res4.status_code == 200
    
    res5 = client.post("/api/simulation/start", json={"simulation_id": "sim_1"})
    assert res5.status_code == 200
    
    res6 = client.post("/api/report/generate", json={"simulation_id": "sim_1"})
    assert res6.status_code == 200
    assert "report_id" in res6.json["data"]
