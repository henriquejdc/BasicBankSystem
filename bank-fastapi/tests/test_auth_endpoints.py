import pytest
from httpx import AsyncClient
from src.main import app
import asyncio

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={"user_id": 123})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

