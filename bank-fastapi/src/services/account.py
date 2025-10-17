from databases.interfaces import Record

from src.database import database
from src.models.account import accounts
from src.schemas.account import AccountIn


class AccountService:
    """
    Serviço responsável pelas operações de conta corrente no banco de dados.
    """
    async def read_all(self, limit: int, skip: int = 0) -> list[Record]:
        """
        Lista todas as contas com paginação.
        :param limit: número máximo de contas a retornar
        :param skip: número de contas a pular
        :return: lista de contas
        """
        query = accounts.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, account: AccountIn) -> Record:
        """
        Cria uma nova conta corrente.
        :param account: dados da conta
        :return: conta criada
        """
        command = accounts.insert().values(user_id=account.user_id, balance=account.balance)
        account_id = await database.execute(command)

        query = accounts.select().where(accounts.c.id == account_id)
        return await database.fetch_one(query)
