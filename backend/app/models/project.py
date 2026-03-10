import uuid
import json
import os
import threading
from app.config import Config

class ProjectManager:
    _lock = threading.Lock()

    @staticmethod
    def create_project(name: str) -> dict:
        project_id = f"proj_{uuid.uuid4().hex[:8]}"
        project_data = {"project_id": project_id, "name": name, "files": []}
        project_path = os.path.join(Config.PROJECT_DIR, f"{project_id}.json")
        with ProjectManager._lock:
            with open(project_path, "w", encoding="utf-8") as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
        return project_data

    @staticmethod
    def get_project(project_id: str) -> dict:
        project_path = os.path.join(Config.PROJECT_DIR, f"{project_id}.json")
        with ProjectManager._lock:
            if not os.path.exists(project_path):
                return None
            with open(project_path, "r", encoding="utf-8") as f:
                return json.load(f)
                
    @staticmethod
    def add_file_to_project(project_id: str, file_path: str):
        project_path = os.path.join(Config.PROJECT_DIR, f"{project_id}.json")
        with ProjectManager._lock:
            if not os.path.exists(project_path):
                return
            with open(project_path, "r", encoding="utf-8") as f:
                project_data = json.load(f)
            project_data["files"].append(file_path)
            with open(project_path, "w", encoding="utf-8") as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def update_graph_interaction(project_id: str, agent_a: str, agent_b: str, interaction_type: str):
        project_path = os.path.join(Config.PROJECT_DIR, f"{project_id}.json")
        if not os.path.exists(project_path):
            return
            
        with ProjectManager._lock:
            with open(project_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            graph = data.get("graph", {"nodes": [], "edges": []})
            
            edge_found = False
            for edge in graph["edges"]:
                if (edge["source"] == agent_a and edge["target"] == agent_b) or \
                   (edge["source"] == agent_b and edge["target"] == agent_a):
                    weight = edge.get("metadata", {}).get("weight", 1)
                    edge.setdefault("metadata", {})["weight"] = weight + 1
                    edge.setdefault("metadata", {}).setdefault("interactions", []).append(interaction_type[:50])
                    if len(edge["metadata"]["interactions"]) > 5:
                        edge["metadata"]["interactions"].pop(0)
                    edge_found = True
                    break
            
            if not edge_found:
                graph["edges"].append({
                    "source": agent_a,
                    "target": agent_b,
                    "type": "social_bond",
                    "metadata": { "weight": 1, "interactions": [interaction_type[:50]] }
                })
            
            data["graph"] = graph
            with open(project_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
