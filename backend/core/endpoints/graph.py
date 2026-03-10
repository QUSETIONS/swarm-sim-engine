from fastapi import APIRouter, File, UploadFile, Form
from typing import List, Optional
from core.domain.project import ProjectManager
import os
import threading
from core.config import Config
from core.utils.file_parser import extract_text
from core.engine.ontology_generator import OntologyGenerator
from core.utils.llm_client import LLMClient
from core.domain.task import TaskManager
from core.engine.semantic_mesh_builder import GraphBuilder

router = APIRouter()

@router.post("/ontology/generate")
async def generate_ontology(
    files: List[UploadFile] = File(...),
    simulation_requirement: Optional[str] = Form("")
):
    project = ProjectManager.create_project("Untitled")
    
    document_texts = []
    for file in files:
        if file.filename:
            file_path = os.path.join(Config.PROJECT_DIR, f"{project['project_id']}_{file.filename}")
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            ProjectManager.add_file_to_project(project["project_id"], file_path)
            document_texts.append(extract_text(file_path))

    llm_client = LLMClient()
    generator = OntologyGenerator(llm_client)
    ontology = generator.generate(document_texts, simulation_requirement or "")

    return {
        "success": True,
        "data": {
            "project_id": project["project_id"],
            "ontology": ontology
        }
    }

@router.post("/build")
async def build_graph(data: dict):
    project_id = data.get("project_id")
    
    task_id = TaskManager.create_task("graph_build")
    thread = threading.Thread(target=GraphBuilder.build_graph, args=(project_id, task_id), daemon=True)
    thread.start()

    return {
        "success": True,
        "data": {
            "task_id": task_id
        }
    }
