import json
import os
from core.config import Config
from core.domain.project import ProjectManager

class GraphEvolver:
    @staticmethod
    def record_interaction(project_id: str, agent_a: str, agent_b: str, interaction_type: str):
        """
        Strengthen or create a social edge between two agents in the world graph.
        """
        ProjectManager.update_graph_interaction(project_id, agent_a, agent_b, interaction_type)
