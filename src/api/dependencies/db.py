from typing import Annotated

from fastapi import Depends

from src.db.database import async_session
from src.utils.transaction import TransactionManager


async def get_db_transaction():
    """
    Provides a transactional database session as a FastAPI dependency.
    This function is a generator that creates and manages a database
    transaction.

    :return: A generator that yields an instance of the transaction manager.
    """

    async with TransactionManager(
        session_factory=async_session,
    ) as transaction:
        yield transaction


DbTransactionDep = Annotated[
    TransactionManager,
    Depends(get_db_transaction),
]
