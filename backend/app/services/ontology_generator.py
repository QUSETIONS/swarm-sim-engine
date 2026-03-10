class OntologyGenerator:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def generate(self, document_texts, simulation_requirement):
        return {
            "entity_types": [{"name": "Person"}],
            "edge_types": [{"name": "RESPONDS_TO"}],
            "analysis_summary": "placeholder",
        }
