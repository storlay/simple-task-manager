from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class TaskDoesNotExistsHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Task does not exists"
