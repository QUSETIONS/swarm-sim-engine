import os

class Config:
    BASE_DIR = os.getcwd()
    PROJECT_DIR = os.path.join(BASE_DIR, "data", "projects")
    TASKS_FILE = os.path.join(BASE_DIR, "data", "tasks.json")
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
