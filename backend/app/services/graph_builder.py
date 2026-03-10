from app.models.task import TaskManager
import time

class GraphBuilder:
    @staticmethod
    def build_graph(project_id: str, task_id: str):
        TaskManager.tasks[task_id]["status"] = "in_progress"
        time.sleep(1) # simulate graph construction
        TaskManager.tasks[task_id]["status"] = "completed"
        TaskManager.tasks[task_id]["graph_id"] = f"graph_{project_id}"
