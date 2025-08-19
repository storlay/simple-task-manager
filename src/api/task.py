import uuid

from fastapi import APIRouter
from fastapi import status

from src.api.dependencies import DbTransactionDep
from src.api.dependencies.pagination import PaginationDep
from src.exceptions.api.task import TaskDoesNotExistsHTTPException
from src.exceptions.service.task import TaskDoesNotExistsServiceException
from src.schemas.base.schemas import BaseHTTPExceptionSchema
from src.schemas.base.schemas import UUIDSchema
from src.schemas.task import TaskCreateSchema
from src.schemas.task import TaskSchema
from src.schemas.task import TaskUpdateSchema
from src.services import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get(
    "",
    response_model=list[TaskSchema],
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    description="Get all tasks with pagination",
)
async def get_all_tasks(
    transaction: DbTransactionDep,
    pagination: PaginationDep,
) -> list[TaskSchema]:
    return await TaskService(transaction).get_all(
        pagination=pagination,
    )


@router.get(
    "/{task_id}",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
    responses={
        TaskDoesNotExistsHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": TaskDoesNotExistsHTTPException.detail,
        },
    },
    summary="Get one task",
    description="Get one task by ID",
)
async def get_one_task(
    task_id: uuid.UUID,
    transaction: DbTransactionDep,
) -> TaskSchema:
    try:
        return await TaskService(transaction).get_one(
            id=task_id,
        )
    except TaskDoesNotExistsServiceException as ex:
        raise TaskDoesNotExistsHTTPException from ex


@router.post(
    "",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add one task",
    description="Add one task",
)
async def add_task(
    transaction: DbTransactionDep,
    data: TaskCreateSchema,
) -> TaskSchema:
    return await TaskService(transaction).create(
        data=data,
    )


@router.patch(
    "/{task_id}",
    response_model=UUIDSchema,
    status_code=status.HTTP_200_OK,
    responses={
        TaskDoesNotExistsHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": TaskDoesNotExistsHTTPException.detail,
        },
    },
    summary="Update one task",
    description="Update one task",
)
async def update_task(
    task_id: uuid.UUID,
    transaction: DbTransactionDep,
    data: TaskUpdateSchema,
) -> UUIDSchema:
    try:
        await TaskService(transaction).update_one(
            task_id=task_id,
            data=data,
        )
    except TaskDoesNotExistsServiceException as ex:
        raise TaskDoesNotExistsHTTPException from ex
    return UUIDSchema(id=task_id)


@router.delete(
    "/{task_id}",
    response_model=UUIDSchema,
    status_code=status.HTTP_200_OK,
    responses={
        TaskDoesNotExistsHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": TaskDoesNotExistsHTTPException.detail,
        },
    },
    summary="Delete one task",
    description="Delete one task",
)
async def delete_task(
    task_id: uuid.UUID,
    transaction: DbTransactionDep,
) -> UUIDSchema:
    try:
        await TaskService(transaction).delete_one(
            task_id=task_id,
        )
    except TaskDoesNotExistsServiceException as ex:
        raise TaskDoesNotExistsHTTPException from ex
    return UUIDSchema(id=task_id)
