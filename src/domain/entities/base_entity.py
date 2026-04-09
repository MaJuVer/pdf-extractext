"""
Clase base para todas las entidades del dominio.

Las entidades son objetos del negocio con identidad única que
persiste a través de los cambios de estado.
"""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class BaseEntity(ABC):
    """
    Clase base abstracta para todas las entidades del dominio.

    Attributes:
        id: Identificador único de la entidad (UUID v4).
        created_at: Timestamp de creación.
        updated_at: Timestamp de última actualización.

    Example:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class User(BaseEntity):
        ...     email: str
        ...     name: str
        >>> user = User(email="user@example.com", name="John")
        >>> user.id  # UUID generado automáticamente
    """

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update_timestamp(self) -> None:
        """Actualiza el timestamp de modificación."""
        self.updated_at = datetime.now(timezone.utc)

    def __eq__(self, other: Any) -> bool:
        """
        Dos entidades son iguales si tienen el mismo tipo e ID.

        Args:
            other: Objeto a comparar.

        Returns:
            True si son la misma entidad, False en caso contrario.
        """
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id and type(self) is type(other)

    def __hash__(self) -> int:
        """Hash basado en el ID de la entidad."""
        return hash(self.id)
