"""
Clase base para mappers.

Los mappers convierten entre DTOs y entidades del dominio,
manteniendo separada la lógica de transformación.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.application.dtos.base_dto import BaseInputDTO, BaseOutputDTO
from src.domain.entities.base_entity import BaseEntity

E = TypeVar("E", bound=BaseEntity)
InDTO = TypeVar("InDTO", bound=BaseInputDTO)
OutDTO = TypeVar("OutDTO", bound=BaseOutputDTO)


class BaseMapper(ABC, Generic[E, InDTO, OutDTO]):
    """
    Clase base para mappers de entidades.

    Convierte entre:
    - InputDTO -> Entity (to_entity)
    - Entity -> OutputDTO (to_dto)

    Type Parameters:
        E: Tipo de entidad.
        InDTO: Tipo de DTO de entrada.
        OutDTO: Tipo de DTO de salida.

    Example:
        >>> class UserMapper(BaseMapper[User, CreateUserDTO, UserOutputDTO]):
        ...     def to_entity(self, dto: CreateUserDTO) -> User:
        ...         return User(email=dto.email, name=dto.name)
        ...
        ...     def to_dto(self, entity: User) -> UserOutputDTO:
        ...         return UserOutputDTO(...)
    """

    @abstractmethod
    def to_entity(self, dto: InDTO) -> E:
        """
        Convierte un DTO de entrada a entidad.

        Args:
            dto: DTO con datos de entrada.

        Returns:
            Entidad del dominio.
        """
        pass

    @abstractmethod
    def to_dto(self, entity: E) -> OutDTO:
        """
        Convierte una entidad a DTO de salida.

        Args:
            entity: Entidad del dominio.

        Returns:
            DTO para presentación.
        """
        pass
