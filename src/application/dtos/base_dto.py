"""
Clase base para Data Transfer Objects.

Los DTOs transportan datos entre capas de la aplicación
sin exponer entidades del dominio.
"""

from dataclasses import dataclass

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
