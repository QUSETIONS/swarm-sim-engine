import pytest
from core.engine.simulation_config_generator import SimulationConfigGenerator

class FakeLLMClient:
    def generate(self, prompt):
        return "{}"

@pytest.fixture
def fake_llm_client():
    return FakeLLMClient()

def test_simulation_config_contains_time_and_agent_settings(fake_llm_client):
    config = SimulationConfigGenerator(llm_client=fake_llm_client).generate_config(
        simulation_id="sim_1",
        project_id="proj_1",
        graph_id="graph_1",
        simulation_requirement="Predict how sentiment evolves",
        entities=[{"uuid": "1", "name": "Alice"}],
    )
    assert config["time_config"]["minutes_per_round"] > 0
    assert len(config["agent_configs"]) == 1
