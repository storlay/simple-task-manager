from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.config import TaskStatus
from src.db import Base
from src.db.mixins import TimestampMixin
from src.db.mixins import UUIDPkMixin


class Task(
    Base,
    UUIDPkMixin,
    TimestampMixin,
):
    name: Mapped[str] = mapped_column(
        String(100),
    )
    description: Mapped[str] = mapped_column(
        String(2000),
        server_default="",
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),
        default=TaskStatus.CREATED,
    )
