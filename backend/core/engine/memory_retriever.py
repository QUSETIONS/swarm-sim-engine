import os
import json
from core.config import Config
from core.domain.project import ProjectManager

class RetrievalTools:
    @staticmethod
    def query_logs(simulation_id: str, project_id: str, agent_id: str, limit: int = 5) -> str:
        """
        Retrieves the last N actions for a specific agent and augments context 
        with GraphRAG semantic relationships from the active project.
        """
        log_path = os.path.join(Config.PROJECT_DIR, f"{simulation_id}_log.jsonl")
        
        # 1. Fetch Graph Relationships (GraphRAG Context)
        graph_context = ""
        try:
            pdata = ProjectManager.get_project(project_id)
            if pdata and "graph" in pdata:
                edges = pdata["graph"].get("edges", [])
                nodes = pdata.get("ontology", {}).get("nodes", [])
                
                # Build a quick lookup for node properties
                node_lookup = {n.get("id"): n for n in nodes}
                
                related_edges = [e for e in edges if e["source"] == agent_id or e["target"] == agent_id]
                if related_edges:
                    graph_context = "\n[GraphRAG Context]: You have topological relationships with these entities:\n"
                    for e in related_edges:
                        other = e["target"] if e["source"] == agent_id else e["source"]
                        weight = e.get("metadata", {}).get("weight", 1)
                        r_type = e.get("type", "related_to")
                        
                        target_node = node_lookup.get(other, {})
                        target_type = target_node.get("type", "Unknown")
                        target_props = target_node.get("properties", {})
                        
                        desc = f"{other} ({target_type})"
                        if target_props:
                            desc += f" - Properties: {target_props}"
                            
                        graph_context += f" - [{r_type}] {desc} (Weight: {weight})\n"
        except Exception:
            pass

        # 2. Fetch Recent Log Stream
        if not os.path.exists(log_path):
            return f"{graph_context}\nNo previous log memories found. You just entered the system."
            
        memories = []
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line in reversed(lines):
                if not line.strip(): continue
                data = json.loads(line)
                if data.get("agent_id") == agent_id or data.get("target_id") == agent_id:
                    tool_res = ""
                    if "Sandbox Execution" in data.get("content", ""):
                        tool_res = " (Tool Execution Logged)"
                    memories.insert(0, f"[Round {data.get('round')}] You {data.get('action')} target '{data.get('target_id')}': '{data.get('content')}'{tool_res}. Thought: '{data.get('thought')}'")
                
                if len(memories) >= limit:
                    break
        except Exception:
            pass
            
        log_context = "\n".join(memories) if memories else "No relevant past logs found."
        
        return f"{graph_context}\n[Recent Action Stream]:\n{log_context}"
