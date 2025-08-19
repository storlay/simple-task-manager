import pytest
from fastapi import status

from src.config import TaskStatus


async def test_create_task(
    ac,
    create_task_data,
):
    response = await ac.post(
        "/tasks",
        json=create_task_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data
    assert response_data["name"] == create_task_data["name"]
    assert response_data["description"] == create_task_data["description"]
    assert response_data["status"] == create_task_data["status"]


@pytest.mark.parametrize(
    "name, description, task_status",
    [
        ("1" * 101, "description", TaskStatus.CREATED),
        ("name", "1" * 2001, TaskStatus.CREATED),
        ("name", "1" * 2001, "norm"),
        (1, "1" * 2001, "norm"),
        ("name", 1, TaskStatus.CREATED),
        ("name", "description", 1),
    ],
)
async def test_create_task_with_invalid_data(
    name,
    description,
    task_status,
    ac,
    populate_db,
):
    create_data = {
        "name": name,
        "description": description,
        "status": task_status,
    }
    response = await ac.post(
        "/tasks",
        json=create_data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
