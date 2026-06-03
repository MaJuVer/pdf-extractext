"""
Excepciones base para el dominio.

Las excepciones de dominio representan errores de negocio.
Siguen una jerarquía clara para permitir manejo específico.
"""

from typing import Optional


class DomainException(Exception):
    """
    Excepción base para errores del dominio.

    Todas las excepciones de negocio deben heredar de esta clase.

    Attributes:
        message: Descripción del error.
        code: Código identificador del error.

    Example:
        >>> raise DomainException("Operación no permitida", code="INVALID_OPERATION")
    """

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        """
        Inicializa la excepción.

        Args:
            message: Mensaje descriptivo del error.
            code: Código identificador opcional.
        """
        super().__init__(message)
        self.message = message
        self.code = code or "DOMAIN_ERROR"

    def __str__(self) -> str:
        """Representación legible de la excepción."""
        return f"[{self.code}] {self.message}"


class EntityNotFoundException(DomainException):
    """
    Entidad no encontrada.

    Raised cuando se busca una entidad que no existe.
    """

    def __init__(self, entity_name: str, entity_id: str) -> None:
        message = f"{entity_name} con ID '{entity_id}' no encontrado"
        super().__init__(message, code="ENTITY_NOT_FOUND")
        self.entity_name = entity_name
        self.entity_id = entity_id


class ValidationException(DomainException):
    """
    Error de validación de datos.

    Raised cuando los datos no cumplen reglas de negocio.
    """

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(message, code="VALIDATION_ERROR")
        self.field = field


class BusinessRuleException(DomainException):
    """
    Violación de regla de negocio.

    Raised cuando se viola una regla del dominio.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, code="BUSINESS_RULE_VIOLATION")


class DocumentoDuplicadoException(DomainException):
    """
    Documento duplicado en el sistema.

    Raised cuando se intenta procesar un documento cuyo hash SHA256
    ya existe en la base de datos, indicando que es un duplicado.
    """

    def __init__(
        self,
        message: str = "El documento ya existe en el sistema",
        *,
        hash_contenido: str | None = None,
    ) -> None:
        """
        Inicializa la excepción con un mensaje y un hash opcional.

        Args:
            message: Mensaje descriptivo del error. Por defecto, una descripción genérica.
            hash_contenido: El hash SHA256 del documento que causó el conflicto.
        """
        super().__init__(message, code="DOCUMENTO_DUPLICADO")
        self.hash_contenido = hash_contenido

    def __str__(self) -> str:
        """Representación legible de la excepción.

        Incluye el hash del contenido si está disponible.
        """
        base = f"[{self.code}] {self.message}"
        if self.hash_contenido is not None:
            base += f" - Hash: {self.hash_contenido}"
        return base
