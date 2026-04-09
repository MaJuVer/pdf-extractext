"""
Interfaz base para todos los repositorios.

Las interfaces de repositorio definen el contrato de acceso a
datos siguiendo el principio de Inversión de Dependencias (DIP).
La infraestructura implementa estas interfaces.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from src.domain.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(ABC, Generic[T]):
    """
        Interfaz base para repositorios.

        Define operaciones CRUD básicas que cualquier repositorio
    debe implementar. La implementación concreta reside en la
    capa de infraestructura.

        Type Parameters:
            T: Tipo de entidad que maneja el repositorio.

        Example:
            >>> class UserRepository(BaseRepository[User]):
            ...     @abstractmethod
            ...     def find_by_email(self, email: str) -> Optional[User]: ...
    """

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Obtiene una entidad por su ID.

        Args:
            entity_id: Identificador único de la entidad.

        Returns:
            La entidad si existe, None en caso contrario.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades.

        Returns:
            Lista de todas las entidades.
        """
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        """
        Agrega una nueva entidad.

        Args:
            entity: Entidad a agregar.

        Returns:
            La entidad persistida con su ID asignado.
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.

        Args:
            entity: Entidad con los datos actualizados.

        Returns:
            La entidad actualizada.
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Elimina una entidad por su ID.

        Args:
            entity_id: Identificador de la entidad a eliminar.

        Returns:
            True si se eliminó, False si no existía.
        """
        pass

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """
        Verifica si existe una entidad con el ID dado.

        Args:
            entity_id: Identificador a verificar.

        Returns:
            True si existe, False en caso contrario.
        """
        pass
