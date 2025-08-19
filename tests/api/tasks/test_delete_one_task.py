import uuid

import pytest
from fastapi import status

from src.exceptions.repository.base import ObjectNotFoundRepoException
from src.schemas.task import TaskSchema


async def test_delete_task(
    ac,
    populate_db,
    db,
):
    task = await db.task.get_all(limit=1, offset=1)
    task: TaskSchema = task[0]

    response = await ac.delete(f"/tasks/{task.id}")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == str(task.id)

    with pytest.raises(ObjectNotFoundRepoException):
        await db.task.get_one(
            query_options=None,
            with_rels=False,
            id=task.id,
        )


async def test_delete_task_with_invalid_task_id(ac):
    response = await ac.delete(f"/tasks/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
