import uuid
from datetime import datetime

from pydantic import BaseModel


class UUIDSchema(BaseModel):
    id: uuid.UUID


class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class BaseHTTPExceptionSchema(BaseModel):
    detail: str
