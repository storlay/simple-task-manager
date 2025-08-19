import uuid

from src.exceptions.repository.base import ObjectNotFoundRepoException
from src.exceptions.service.task import TaskDoesNotExistsServiceException
from src.schemas.pagination import PaginationSchema
from src.schemas.task import TaskCreateSchema
from src.schemas.task import TaskSchema
from src.schemas.task import TaskUpdateSchema
from src.services.base import BaseService


class TaskService(BaseService):
    async def get_one(
        self,
        **filters,
    ) -> TaskSchema:
        """
        Retrieve a single task by given filters.

        :param filters: Arbitrary filters to search for the task
        :raises TaskDoesNotExistsServiceException: If the task is not found
        """

        try:
            return await self.db.task.get_one(
                query_options=None,
                with_rels=False,
                **filters,
            )
        except ObjectNotFoundRepoException as ex:
            raise TaskDoesNotExistsServiceException from ex

    async def get_all(
        self,
        pagination: PaginationSchema,
    ) -> list[TaskSchema]:
        """
        Retrieve a list of tasks with pagination.

        :param pagination: Object containing limit and offset for pagination
        """

        return await self.db.task.get_all(
            pagination.limit,
            pagination.offset,
        )

    async def create(
        self,
        data: TaskCreateSchema,
    ) -> TaskSchema:
        """
        Create a new task.

        :param data: Data required to create a new task
        """

        created_data = await self.db.task.add(data)
        await self.db.commit()
        return created_data

    async def update_one(
        self,
        task_id: uuid.UUID,
        data: TaskUpdateSchema,
    ) -> uuid.UUID:
        """
        Update an existing task.

        :param task_id: ID of the task to update
        :param data: Data to update in the task
        :raises TaskDoesNotExistsServiceException: If the task is not found
        """

        try:
            await self.db.task.update_one(
                data,
                partially=True,
                id=task_id,
            )
            await self.db.commit()
            return task_id
        except ObjectNotFoundRepoException as ex:
            raise TaskDoesNotExistsServiceException from ex

    async def delete_one(
        self,
        task_id: uuid.UUID,
    ) -> None:
        """
        Delete a task.

        :param task_id: ID of the task to delete
        :raises TaskDoesNotExistsServiceException: If the task is not found
        """

        try:
            await self.db.task.delete_one(
                id=task_id,
            )
            await self.db.commit()
        except ObjectNotFoundRepoException as ex:
            raise TaskDoesNotExistsServiceException from ex
