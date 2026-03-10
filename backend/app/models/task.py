import uuid
import json
import os
import threading
from app.config import Config

class TaskManager:
    _lock = threading.Lock()
    tasks = {}

    @staticmethod
    def _load():
        with TaskManager._lock:
            if os.path.exists(Config.TASKS_FILE):
                try:
                    with open(Config.TASKS_FILE, "r", encoding="utf-8") as f:
                        TaskManager.tasks = json.load(f)
                except Exception:
                    TaskManager.tasks = {}

    @staticmethod
    def _save():
        with TaskManager._lock:
            with open(Config.TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(TaskManager.tasks, f, ensure_ascii=False, indent=2)

    @staticmethod
    def create_task(task_type: str) -> str:
        TaskManager._load()
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        with TaskManager._lock:
            TaskManager.tasks[task_id] = {"status": "pending", "type": task_type}
        TaskManager._save()
        return task_id

    @staticmethod
    def update_status(task_id: str, status: str):
        TaskManager._load()
        with TaskManager._lock:
            if task_id in TaskManager.tasks:
                TaskManager.tasks[task_id]["status"] = status
        TaskManager._save()

    @staticmethod
    def get_task(task_id: str):
        TaskManager._load()
        with TaskManager._lock:
            return TaskManager.tasks.get(task_id)
