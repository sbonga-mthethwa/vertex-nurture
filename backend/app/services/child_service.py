from datetime import date
from uuid import UUID

from app.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from app.models.child import Child
from app.repositories.child_repository import ChildRepository
from app.services.base import BaseService


class ChildService(BaseService):
    """
    Business logic for child management.
    """

    def __init__(
        self,
        repository: ChildRepository,
    ):
        super().__init__(repository.db)

        self.repository = repository

    async def list_children(
        self,
        parent_id: UUID,
    ) -> list[Child]:
        """
        Returns all active children belonging to a parent.
        """

        return await self.repository.get_active_by_parent(
            parent_id,
        )

    async def get_child(
        self,
        child_id: UUID,
        parent_id: UUID,
    ) -> Child:
        """
        Returns a single child belonging to the parent.
        """

        child = await self.repository.get_by_id(
            child_id,
        )

        if child is None:
            raise NotFoundError(
                "Child not found."
            )

        if child.parent_id != parent_id:
            raise NotFoundError(
                "Child not found."
            )

        return child

    async def create_child(
        self,
        parent_id: UUID,
        first_name: str,
        surname: str | None,
        date_of_birth: date,
        gender,
        birth_weight,
        birth_height,
        blood_group,
        allergies,
        medical_conditions,
    ) -> Child:
        """
        Creates a child.
        """

        if date_of_birth > date.today():
            raise ValidationError(
                "Date of birth cannot be in the future."
            )

        child = Child(
            parent_id=parent_id,
            first_name=first_name,
            surname=surname,
            date_of_birth=date_of_birth,
            gender=gender,
            birth_weight=birth_weight,
            birth_height=birth_height,
            blood_group=blood_group,
            allergies=allergies,
            medical_conditions=medical_conditions,
            is_active=True,
        )

        return await self.repository.create(
            child,
        )

    async def update_child(
        self,
        child_id: UUID,
        parent_id: UUID,
        request,
    ) -> Child:
        """
        Updates a child.
        """

        child = await self.get_child(
            child_id,
            parent_id,
        )

        if (
            request.date_of_birth
            and request.date_of_birth > date.today()
        ):
            raise ValidationError(
                "Date of birth cannot be in the future."
            )

        for field, value in request.model_dump(
            exclude_unset=True,
        ).items():

            setattr(
                child,
                field,
                value,
            )

        return await self.repository.update(
            child,
        )

    async def delete_child(
        self,
        child_id: UUID,
        parent_id: UUID,
    ) -> None:
        """
        Soft delete.
        """

        child = await self.get_child(
            child_id,
            parent_id,
        )

        child.is_active = False

        await self.repository.update(
            child,
        )