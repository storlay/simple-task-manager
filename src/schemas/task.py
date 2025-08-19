from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel

from src.config import TaskStatus
from src.schemas.base.schemas import TimestampSchema
from src.schemas.base.schemas import UUIDSchema


class TaskCreateSchema(BaseModel):
    name: Annotated[
        str,
        MaxLen(100),
    ]
    description: Annotated[
        str,
        MaxLen(100),
    ]
    status: TaskStatus


class TaskUpdateSchema(BaseModel):
    name: Annotated[
        str | None,
        MaxLen(100),
    ]
    description: Annotated[
        str | None,
        MaxLen(100),
    ]
    status: TaskStatus | None


class TaskSchema(
    UUIDSchema,
    TimestampSchema,
    TaskCreateSchema,
):
    pass
