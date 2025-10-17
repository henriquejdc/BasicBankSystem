import pytest
from src.services.account import AccountService
from src.schemas.account import AccountIn
from src.database import database
import asyncio

@pytest.mark.asyncio
async def test_create_and_read_account(monkeypatch):
    # Setup: limpar tabela antes do teste (idealmente usar um banco isolado)
    await database.execute("DELETE FROM accounts")
    service = AccountService()
    account_in = AccountIn(user_id=1, balance=100.0)
    created = await service.create(account_in)
    assert created['user_id'] == 1
    assert float(created['balance']) == 100.0

    accounts = await service.read_all(limit=10)
    assert any(acc['user_id'] == 1 for acc in accounts)

