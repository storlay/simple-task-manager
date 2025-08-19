from typing import Any
from typing import Generic
from typing import Iterable
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.db import Base
from src.exceptions.repository.base import CannotAddObjectRepoException
from src.exceptions.repository.base import ObjectNotFoundRepoException
from src.repositories.mappers.base import BaseDataMapper


SchemaType = TypeVar(
    "SchemaType",
    bound=BaseModel,
)


class BaseRepository(Generic[SchemaType]):
    """
    Base class for data repositories.
    Provides a common interface for CRUD operations.
    """

    model: type[Base] = None  # type: ignore
    mapper: type[BaseDataMapper] = None  # type: ignore

    def __init__(
        self,
        session: AsyncSession,
    ):
        """
        Initialize the repository with a database session.

        :param session: The asynchronous SQLAlchemy session.
        """

        self.session = session

    async def get_all(
        self,
        limit: int,
        offset: int,
    ) -> list[SchemaType | Any]:
        """
        Get all entities with pagination.

        :param limit: The maximum number of entities to return.
        :param offset: The number of entities to skip.
        :return: A list of domain entities.
        """

        query = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(query)
        # fmt: off
        return [
            self.mapper.map_to_domain_entity(model)
            for model in result.scalars().all()
        ]
        # fmt: on

    async def get_one_or_none(
        self,
        **filter_by,
    ) -> SchemaType | None | Any:
        """
        Get a single entity by filter criteria or return None if not found.

        :param filter_by: Keyword arguments to filter the query (e.g., id=1).
        :return: A domain entity or None if no entity is found.
        """

        # fmt: off
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return model
        return self.mapper.map_to_domain_entity(model)

    async def get_one(
        self,
        query_options: Iterable[ExecutableOption] | None = None,
        with_rels: bool = False,
        **filter_by,
    ) -> SchemaType | Any:
        """
        Get a single entity by filter criteria. Raises an exception if not found.

        :param query_options: SQLAlchemy query options (e.g., for eager loading).
        :param with_rels: If True, map the entity with its relationships.
        :param filter_by: Keyword arguments to filter the query.
        :return: The found domain entity.
        :raises ObjectNotFoundRepoException: If no entity is found.
        """

        # fmt: off
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        if query_options is not None:
            query = query.options(*query_options)
        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound as ex:
            raise ObjectNotFoundRepoException from ex

        return self.mapper.map_to_domain_entity(model, with_rels=with_rels)

    async def add(
        self,
        data: SchemaType,
    ) -> SchemaType | Any:
        """
        Add a new entity to the database.

        :param data: A Pydantic model containing the data for the new entity.
        :return: The newly created domain entity.
        :raises CannotAddObjectRepoException: If the entity cannot be added,
                                              e.g., due to a unique constraint violation.
        """

        # fmt: off
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        # fmt: on
        try:
            result = await self.session.execute(stmt)
            model = result.scalar_one()
        except IntegrityError as ex:
            raise CannotAddObjectRepoException from ex
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(
        self,
        data: list[SchemaType],
    ) -> None:
        """
        Add multiple entities to the database in a single operation.

        :param data: A list of Pydantic models to be added.
        :raises CannotAddObjectRepoException: If entities cannot be added.
        """

        # fmt: off
        stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
        )
        # fmt: on
        try:
            await self.session.execute(stmt)
        except IntegrityError as ex:
            raise CannotAddObjectRepoException from ex

    async def update_one(
        self,
        data: SchemaType,
        partially: bool = False,
        **filter_by,
    ) -> int:
        """
        Update a single entity matching the filter criteria.

        :param data: A Pydantic model with the new data.
        :param partially: If True, performs a partial update (excludes unset fields).
        :param filter_by: Keyword arguments to find the entity to update.
        :return: The ID of the updated entity.
        :raises ObjectNotFoundRepoException: If no entity matching the filter is found.
        """

        # fmt: off
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=partially))
            .filter_by(**filter_by)
            .returning(self.model.id)  # type: ignore
        )
        # fmt: on
        result = await self.session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound as ex:
            raise ObjectNotFoundRepoException from ex

    async def delete_one(
        self,
        **filter_by,
    ) -> int:
        """
        Delete a single entity matching the filter criteria.

        :param filter_by: Keyword arguments to find the entity to delete.
        :return: The ID of the deleted entity.
        :raises ObjectNotFoundRepoException: If no entity matching the filter is found.
        """

        # fmt: off
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
            .returning(self.model.id)  # type: ignore
        )
        # fmt: on
        result = await self.session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound as ex:
            raise ObjectNotFoundRepoException from ex

    async def delete_bulk(
        self,
        **filter_by,
    ) -> None:
        """
        Delete multiple entities matching the filter criteria.

        :param filter_by: Keyword arguments to find the entities to delete.
        """

        # fmt: off
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        await self.session.execute(stmt)
