import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_create_and_list_accounts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Login para obter token
        login_resp = await ac.post("/auth/login", json={"user_id": 456})
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Criar conta
        resp = await ac.post("/accounts/", json={"user_id": 456, "balance": 200.0}, headers=headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["user_id"] == 456
        assert float(data["balance"]) == 200.0

        # Listar contas
        resp = await ac.get("/accounts/?limit=10&skip=0", headers=headers)
        assert resp.status_code == 200
        contas = resp.json()
        assert any(acc["user_id"] == 456 for acc in contas)

