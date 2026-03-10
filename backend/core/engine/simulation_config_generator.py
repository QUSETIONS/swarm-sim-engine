class SimulationConfigGenerator:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def generate_config(self, simulation_id, project_id, graph_id, simulation_requirement, entities):
        return {
            "time_config": {"minutes_per_round": 60, "total_simulation_hours": 24},
            "agent_configs": [{"agent_id": i+1} for i, _ in enumerate(entities)],
            "event_config": {"initial_posts": []},
            "platform_config": {"feed_type": "single_platform"},
        }
