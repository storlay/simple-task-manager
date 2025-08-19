from src.models.task import Task
from src.repositories.base import BaseRepository
from src.repositories.mappers.task import TaskDataMapper


class TaskRepository(BaseRepository):
    model = Task
    mapper = TaskDataMapper
