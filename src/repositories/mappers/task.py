from src.models.task import Task
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.task import TaskSchema


class TaskDataMapper(BaseDataMapper):
    model = Task
    schema = TaskSchema
