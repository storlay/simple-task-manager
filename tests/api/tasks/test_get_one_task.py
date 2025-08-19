import uuid

from fastapi import status

from src.schemas.task import TaskSchema


async def test_get_one_task(
    ac,
    populate_db,
    db,
):
    task = await db.task.get_all(limit=1, offset=1)
    task: TaskSchema = task[0]
    response = await ac.get(f"/tasks/{task.id}")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert response_data["name"] == task.name
    assert response_data["description"] == task.description
    assert response_data["status"] == task.status
    assert response_data["created_at"]
    assert response_data["updated_at"]


async def test_get_non_existent_task(ac):
    response = await ac.get(f"/tasks/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
