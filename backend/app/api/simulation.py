from fastapi import APIRouter, HTTPException
from app.services.profile_generator import ProfileGenerator
from app.services.simulation_config_generator import SimulationConfigGenerator
from app.utils.llm_client import LLMClient
from app.models.task import TaskManager
from app.services.simulation_runner import SimulationRunner
import threading

router = APIRouter()

@router.post("/profiles/generate")
async def generate_profiles(data: dict):
    entities = data.get("entities", [])
    
    generator = ProfileGenerator()
    profiles = generator.generate_profiles(entities)
    
    return {
        "success": True,
        "data": {
            "profiles": profiles
        }
    }

@router.post("/config/generate")
async def generate_config(data: dict):
    simulation_id = data.get("simulation_id", "sim_0")
    project_id = data.get("project_id", "proj_0")
    graph_id = data.get("graph_id", "graph_0")
    simulation_requirement = data.get("simulation_requirement", "")
    entities = data.get("entities", [])
    
    llm_client = LLMClient()
    generator = SimulationConfigGenerator(llm_client)
    config = generator.generate_config(
        simulation_id=simulation_id,
        project_id=project_id,
        graph_id=graph_id,
        simulation_requirement=simulation_requirement,
        entities=entities
    )
    
    return {
        "success": True,
        "data": {
            "config": config
        }
    }

@router.post("/start")
async def start_simulation(data: dict):
    simulation_id = data.get("simulation_id")
    project_id = data.get("project_id", "demo_project")
    
    task_id = TaskManager.create_task("simulation_run")
    thread = threading.Thread(target=SimulationRunner.start, args=(simulation_id, task_id, project_id), daemon=True)
    thread.start()
    
    return {
        "success": True,
        "data": {
            "task_id": task_id,
            "runner_status": "starting"
        }
    }

@router.post("/interview")
async def interview_agent(data: dict):
    return {
        "success": True,
        "data": {
            "response": "Hello, I am a simulated agent response."
        }
    }

@router.post("/stop")
async def stop_simulation(data: dict):
    task_id = data.get("task_id")
    if not task_id:
        raise HTTPException(status_code=400, detail={"success": False, "error": "task_id is required"})
        
    TaskManager.update_status(task_id, "stopped")
    return {
        "success": True,
        "data": {
            "status": "simulation_stopping"
        }
    }

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = TaskManager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"success": False, "error": "Task not found", "data": None})
    return {"success": True, "data": task, "error": None}
