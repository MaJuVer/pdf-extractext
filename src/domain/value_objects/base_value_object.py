"""
Clase base para objetos de valor del dominio.

Los objetos de valor son inmutables y se identifican únicamente
por sus atributos. No tienen identidad propia.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any


@dataclass(frozen=True)
class BaseValueObject(ABC):
    """
    Clase base abstracta para objetos de valor.

    Los objetos de valor son inmutables (frozen=True) y se
    identifican por sus atributos, no por un ID único.

    Example:
        >>> from dataclasses import dataclass
        >>> @dataclass(frozen=True)
        ... class Email(BaseValueObject):
        ...     address: str
        ...     def _validate(self) -> None:
        ...         if "@" not in self.address:
        ...             raise ValueError("Invalid email")
        >>> email = Email("user@example.com")
    """

    def __post_init__(self) -> None:
        """Valida el objeto después de la creación."""
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """
        Valida las reglas de negocio del objeto de valor.

        Raises:
            ValueError: Si las reglas de validación no se cumplen.
        """
        pass

    def __eq__(self, other: Any) -> bool:
        """
        Dos objetos de valor son iguales si tienen los mismos atributos.

        Args:
            other: Objeto a comparar.

        Returns:
            True si son iguales, False en caso contrario.
        """
        if not isinstance(other, BaseValueObject):
            return False
        if type(self) is not type(other):
            return False
        return all(
            getattr(self, field.name) == getattr(other, field.name)
            for field in fields(self)
        )

    def __hash__(self) -> int:
        """Hash basado en los atributos del objeto."""
        return hash(tuple(getattr(self, field.name) for field in fields(self)))
