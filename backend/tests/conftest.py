import pytest
from core import create_app
import os
import shutil
import time
from core.config import Config

@pytest.fixture
def app():
    # Use a temporary directory for tests
    test_data_dir = os.path.join(os.getcwd(), "data_test")
    os.makedirs(test_data_dir, exist_ok=True)
    Config.PROJECT_DIR = test_data_dir
    
    app = create_app()

    yield app
    
    # Wait a bit for any background threads to finish using files (important on Windows)
    time.sleep(0.5)
    
    # Cleanup after tests
    if os.path.exists(test_data_dir):
        try:
            shutil.rmtree(test_data_dir, ignore_errors=True)
        except Exception:
            pass

from fastapi.testclient import TestClient

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def prepared_simulation():
    # Helper to create a dummy simulation id
    return "sim_test_123"
