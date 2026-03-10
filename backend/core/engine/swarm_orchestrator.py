from core.domain.task import TaskManager
from core.domain.project import ProjectManager
from core.engine.persona_cortex import AgentLogic
import time
import os
import json
import datetime
from core.config import Config
from loguru import logger

class SimulationRunner:
    @staticmethod
    def start(simulation_id: str, task_id: str, project_id: str = "demo_project"):
        try:
            TaskManager.update_status(task_id, "running")
            
            project_data = ProjectManager.get_project(project_id)
            if not project_data:
                logger.error(f"Project {project_id} not found", simulation_id=simulation_id)
                raise ValueError(f"Project {project_id} not found")
                
            # Fetch agents from project data (instead of hardcoding)
            agents = project_data.get("agents", [])
            if not agents:
                # Fallback to demo agents if none found, but log warning
                agents = [
                    {"uuid": "1", "name": "Alice", "summary": "Researcher"},
                    {"uuid": "2", "name": "Bob", "summary": "Engineer"}
                ]
            
            log_filename = f"{simulation_id}_log.jsonl"
            log_path = os.path.join(Config.PROJECT_DIR, log_filename)
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            
            from concurrent.futures import ThreadPoolExecutor
            
            with open(log_path, "w", encoding="utf-8") as f:
                round_idx = 1
                while True:
                    # Check if requested to stop
                    task = TaskManager.get_task(task_id)
                    if task and task.get("status") in ["stopped", "completed", "failed"]:
                        break

                    def run_agent(agent):
                        try:
                            context = f"Round {round_idx} in the swarm simulation."
                            action = AgentLogic.generate_action(simulation_id, project_id, agent, context)
                            
                            entry = {
                                "timestamp": datetime.datetime.now().isoformat(),
                                "round": round_idx,
                                **action
                            }
                            
                            # Social Evolution
                            target_id = action.get("target_id")
                            if target_id:
                                from core.engine.graph_evolver import GraphEvolver
                                GraphEvolver.record_interaction(project_id, agent["uuid"], target_id, action.get("content", ""))
                            
                            from core.endpoints.ws import manager
                            import asyncio
                            try:
                                asyncio.run(manager.broadcast_to_simulation(simulation_id, entry))
                            except Exception as ws_e:
                                logger.warning(f"WS broadcast failed", error=str(ws_e), simulation_id=simulation_id)
                            
                            return entry
                        except Exception as e:
                            return {"error": str(e), "agent_id": agent.get("uuid"), "round": round_idx}

                    with ThreadPoolExecutor(max_workers=min(len(agents), 10)) as executor:
                        results = list(executor.map(run_agent, agents))
                    
                    for entry in results:
                        if "error" not in entry:
                            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    
                    f.flush()
                    round_idx += 1
                    time.sleep(2) # Give the LLMs and UI a moment to breathe
                    
            if TaskManager.get_task(task_id).get("status") == "running":
                TaskManager.update_status(task_id, "completed")
                logger.info(f"Simulation completed", simulation_id=simulation_id, rounds=round_idx - 1)
        except Exception as e:
            TaskManager.update_status(task_id, "failed")
            logger.exception(f"Simulation failed", simulation_id=simulation_id, error=str(e))
