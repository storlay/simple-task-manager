from typing import Annotated

from annotated_types import MaxLen

from src.config import TaskStatus
from src.schemas.base.schemas import TimestampSchema
from src.schemas.base.schemas import UUIDSchema


class TaskSchema(UUIDSchema, TimestampSchema):
    name: Annotated[
        str,
        MaxLen(100),
    ]
    description: Annotated[
        str,
        MaxLen(100),
    ]
    status: TaskStatus
