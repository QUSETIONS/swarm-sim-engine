import os
import json
import time
from app.models.task import TaskManager
from app.config import Config

def test_task_manager_persistence():
    # Clear existing tasks file
    if os.path.exists(Config.TASKS_FILE):
        os.remove(Config.TASKS_FILE)
    
    # Create a task
    task_id = TaskManager.create_task("test_persist")
    
    # Verify it exists in memory and file
    task = TaskManager.get_task(task_id)
    assert task["status"] == "pending"
    assert os.path.exists(Config.TASKS_FILE)
    
    # Manually load into another "instance" or force reload
    TaskManager.tasks = {} # Clear memory
    task_reloaded = TaskManager.get_task(task_id)
    assert task_reloaded["status"] == "pending"
    
    # Update status and verify persistence
    TaskManager.update_status(task_id, "done")
    TaskManager.tasks = {} # Clear memory
    task_final = TaskManager.get_task(task_id)
    assert task_final["status"] == "done"
