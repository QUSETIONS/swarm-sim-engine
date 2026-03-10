import pytest
from core.domain.project import ProjectManager

@pytest.fixture
def seeded_project():
    return ProjectManager.create_project("Test Project")

def test_build_graph_creates_async_task(client, seeded_project):
    response = client.post("/api/graph/build", json={"project_id": seeded_project["project_id"]})
    assert response.status_code == 200
    assert "task_id" in response.json()["data"]
