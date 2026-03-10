import pytest

@pytest.fixture
def prepared_simulation():
    class SimInfo:
        simulation_id = "sim_test_1"
    return SimInfo()

def test_start_simulation_returns_running_state(client, prepared_simulation):
    response = client.post("/api/simulation/start", json={"simulation_id": prepared_simulation.simulation_id})
    assert response.status_code == 200
    assert response.json["data"]["runner_status"] in {"starting", "running", "pending"}
