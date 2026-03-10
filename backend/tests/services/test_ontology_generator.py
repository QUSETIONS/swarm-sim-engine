import pytest
from core.engine.ontology_generator import OntologyGenerator

class FakeLLMClient:
    def generate(self, prompt):
        return "{}"

@pytest.fixture
def fake_llm_client():
    return FakeLLMClient()

def test_ontology_generator_returns_entities_and_edges(fake_llm_client):
    generator = OntologyGenerator(llm_client=fake_llm_client)
    result = generator.generate(
        document_texts=["Campus conflict discussion"],
        simulation_requirement="Predict public reaction",
    )
    assert "entity_types" in result
    assert "edge_types" in result
