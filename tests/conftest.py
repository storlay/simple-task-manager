import pytest
from httpx import ASGITransport
from httpx import AsyncClient

from src.api.dependencies.db import get_db_transaction
from src.config import TaskStatus
from src.config import settings
from src.db import Base
from src.db.database import async_engine_null_pull
from src.db.database import async_session_null_pool
from src.main import app
from src.schemas.task import TaskCreateSchema
from src.utils.transaction import TransactionManager


async def get_test_db():
    async with TransactionManager(
        session_factory=async_session_null_pool,
    ) as transaction:
        yield transaction


app.dependency_overrides[get_db_transaction] = get_test_db


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.app.mode == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def prepare_db(check_test_mode):
    async with async_engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
async def db(prepare_db):
    async for db in get_test_db():
        yield db


@pytest.fixture(scope="session")
async def populate_db():
    tasks_to_add = [
        TaskCreateSchema(
            name="Task 1",
            description="Task 1 description",
            status=TaskStatus.CREATED,
        ),
        TaskCreateSchema(
            name="Task 2",
            description="Task 2 description",
            status=TaskStatus.IN_PROGRESS,
        ),
        TaskCreateSchema(
            name="Task 3",
            description="Task 3 description",
            status=TaskStatus.COMPLETED,
        ),
    ]
    async with TransactionManager(
        session_factory=async_session_null_pool,
    ) as transaction:
        await transaction.task.add_bulk(tasks_to_add)
        await transaction.commit()
