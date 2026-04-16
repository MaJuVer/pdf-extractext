"""
Clase base para Data Transfer Objects.

Los DTOs transportan datos entre capas de la aplicación
sin exponer entidades del dominio.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class BaseInputDTO:
    """
    DTO base para datos de entrada.

    Los input DTOs son inmutables y validan datos entrantes.

    Example:
        >>> @dataclass(frozen=True)
        ... class CreateUserInputDTO(BaseInputDTO):
        ...     email: str
        ...     name: str
        ...     password: str
    """

    pass


@dataclass(frozen=True)
class BaseOutputDTO:
    """
    DTO base para datos de salida.

    Los output DTOs presentan datos de entidades al exterior.

    Attributes:
        id: Identificador único.
        created_at: Timestamp de creación.
        updated_at: Timestamp de última actualización.

    Example:
        >>> @dataclass(frozen=True)
        ... class UserOutputDTO(BaseOutputDTO):
        ...     email: str
        ...     name: str
    """

    id: UUID
    created_at: datetime
    updated_at: datetime
