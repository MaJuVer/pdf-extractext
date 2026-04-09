"""
Clase base para servicios de aplicación.

Los servicios de aplicación orquestan casos de uso sin contener
lógica de negocio. Coordinan entidades y repositorios.
"""

from abc import ABC
from typing import Generic, TypeVar

from src.domain.repositories.base_repository import BaseRepository

T = TypeVar("T")
R = TypeVar("R", bound=BaseRepository)


class BaseService(ABC, Generic[T, R]):
    """
    Clase base para servicios de aplicación.

    Los servicios de aplicación coordinan entidades del dominio
    y repositorios para ejecutar casos de uso específicos.
    No deben contener lógica de negocio compleja.

    Type Parameters:
        T: Tipo de DTO de entrada.
        R: Tipo de repositorio.

    Attributes:
        repository: Repositorio para acceso a datos.

    Example:
        >>> class CreateUserService(BaseService[CreateUserDTO, UserRepository]):
        ...     def execute(self, dto: CreateUserDTO) -> User:
        ...         user = User(email=dto.email, name=dto.name)
        ...         return self.repository.add(user)
    """

    def __init__(self, repository: R) -> None:
        """
        Inicializa el servicio con su repositorio.

        Args:
            repository: Repositorio para acceso a datos.
        """
        self._repository = repository

    @property
    def repository(self) -> R:
        """Obtiene el repositorio asociado."""
        return self._repository
