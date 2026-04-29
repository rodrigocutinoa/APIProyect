import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from uuid import uuid4

from src.main import app


@pytest.mark.asyncio
async def test_project_and_task_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        project_name = f"test-project-{uuid4().hex}"
        response = await client.post(
            "/api/v1/projects",
            json={"name": project_name, "description": "Proyecto de prueba", "status": "active"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        project = response.json()
        project_id = project["_id"]
        assert project["name"] == project_name

        response = await client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["_id"] == project_id

        response = await client.put(
            f"/api/v1/projects/{project_id}",
            json={"description": "Proyecto actualizado", "status": "paused"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "paused"

        task_title = f"test-task-{uuid4().hex}"
        response = await client.post(
            "/api/v1/tasks",
            json={
                "project_id": project_id,
                "title": task_title,
                "description": "Tarea de prueba",
                "status": "todo",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        task = response.json()
        task_id = task["_id"]
        assert task["project_id"] == project_id
        assert task["title"] == task_title

        response = await client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == task_title

        response = await client.get(f"/api/v1/projects/{project_id}/tasks")
        assert response.status_code == status.HTTP_200_OK
        tasks_by_project = response.json()
        assert any(item["_id"] == task_id for item in tasks_by_project)

        response = await client.get(
            "/api/v1/tasks",
            params={"project_id": project_id, "status": "todo"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert any(item["_id"] == task_id for item in response.json())

        response = await client.put(
            f"/api/v1/tasks/{task_id}",
            json={"status": "in_progress", "priority": "high"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "in_progress"
        assert response.json()["priority"] == "high"

        response = await client.delete(f"/api/v1/tasks/{task_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["deleted"] is True

        response = await client.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["deleted"] is True
