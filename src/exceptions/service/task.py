from src.exceptions.service.base import BaseServiceException


class TaskAlreadyExistsServiceException(BaseServiceException):
    detail = "Task already exists"


class TaskDoesNotExistsServiceException(BaseServiceException):
    detail = "Task does not exists"
