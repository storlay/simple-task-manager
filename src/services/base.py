from src.utils.transaction import TransactionManager


class BaseService:
    """
    Base class for application services.
    """

    def __init__(
        self,
        db: TransactionManager | None = None,
    ) -> None:
        """
        Initialize the service with a transaction manager.

        :param db: The transaction manager instance for handling
                   database sessions and transactions.
        """

        self._db = db

    @property
    def db(self) -> TransactionManager:
        if self._db is None:
            raise RuntimeError(
                "Database connection is required for this operation, "
                "but was not configured."
            )
        return self._db
