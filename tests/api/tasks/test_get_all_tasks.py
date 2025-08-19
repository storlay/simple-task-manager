import pytest
from fastapi import status

from src.config import settings


async def test_get_tasks(
    ac,
    populate_db,
):
    response = await ac.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()


@pytest.mark.parametrize(
    "page, per_page",
    [
        (1, settings.pagination.max_entities_per_page + 1),
        (-1, 1),
    ],
)
async def test_get_tasks_with_invalid_pagination_params(
    page,
    per_page,
    ac,
    populate_db,
):
    response = await ac.get(
        "/tasks",
        params={
            "page": page,
            "per_page": per_page,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
