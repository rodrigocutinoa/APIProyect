import pytest
from httpx import AsyncClient
from fastapi import status

from src.main import app


@pytest.mark.asyncio
async def test_root_and_crud_flow():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/items", json={"name": "test", "description": "desc", "metadata": {"foo": "bar"}})
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "test"
        item_id = data["_id"]

        response = await client.get(f"/items/{item_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "test"

        response = await client.put(f"/items/{item_id}", json={"description": "updated"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["description"] == "updated"

        response = await client.delete(f"/items/{item_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["deleted"] is True
