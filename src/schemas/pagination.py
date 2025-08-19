from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from src.config import settings


class PaginationRequestSchema(BaseModel):
    page: Annotated[
        int,
        Query(
            1,
            ge=1,
        ),
    ]
    per_page: Annotated[
        int,
        Query(
            3,
            ge=1,
            le=settings.pagination.max_entities_per_page,
        ),
    ]


class PaginationSchema(BaseModel):
    limit: int
    offset: int
