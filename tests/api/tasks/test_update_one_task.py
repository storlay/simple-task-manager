import uuid

import pytest
from fastapi import status

from src.config import TaskStatus
from src.schemas.task import TaskSchema


@pytest.mark.parametrize(
    "name, description, task_status",
    [
        ("New name", "New description", TaskStatus.IN_PROGRESS),
        ("New 2 name", "New 2 description", None),
        ("New 3 name", None, None),
        (None, "New 3 description", None),
        (None, None, TaskStatus.COMPLETED),
    ],
)
async def test_update_task(
    name,
    description,
    task_status,
    ac,
    populate_db,
    db,
):
    update_data = {}
    if name:
        update_data["name"] = name
    if description:
        update_data["description"] = description
    if task_status:
        update_data["status"] = task_status

    task = await db.task.get_all(limit=1, offset=1)
    task: TaskSchema = task[0]

    response = await ac.patch(
        f"/tasks/{task.id}",
        json=update_data,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == str(task.id)
    updated_task: TaskSchema = await db.task.get_one(
        query_options=None,
        with_rels=False,
        id=task.id,
    )
    if name:
        assert updated_task.name == update_data["name"]
    if description:
        assert updated_task.description == update_data["description"]
    if task_status:
        assert updated_task.status == update_data["status"]


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
async def test_update_task_with_invalid_data(
    name,
    description,
    task_status,
    ac,
    populate_db,
    db,
):
    update_data = {
        "name": name,
        "description": description,
        "status": task_status,
    }
    task = await db.task.get_all(limit=1, offset=1)
    task: TaskSchema = task[0]
    response = await ac.patch(
        f"/tasks/{task.id}",
        json=update_data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_update_task_with_invalid_task_id(ac):
    update_data = {
        "name": "name",
    }
    response = await ac.patch(
        f"/tasks/{uuid.uuid4()}",
        json=update_data,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
