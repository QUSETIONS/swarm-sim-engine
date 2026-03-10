import pytest

@pytest.fixture
def completed_simulation():
    class SimInfo:
        simulation_id = "sim_test_completed"
    return SimInfo()

def test_generate_report_returns_report_id(client, completed_simulation):
    response = client.post("/api/report/generate", json={"simulation_id": completed_simulation.simulation_id})
    assert response.status_code == 200
    assert response.json()["data"]["report_id"].startswith("report_")
