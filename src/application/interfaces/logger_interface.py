"""
Interfaz para servicios de logging.

Define el contrato que cualquier implementación de logging
debe cumplir, permitiendo cambiar la implementación sin
afectar el resto del código.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class LoggerInterface(ABC):
    """
    Interfaz para servicios de logging.

    Define operaciones de logging que pueden ser implementadas
    por diferentes backends (console, file, cloud, etc.).

    Example:
        >>> logger = get_logger()  # Implementación concreta
        >>> logger.info("Usuario creado", user_id="123")
    """

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """
        Log a nivel DEBUG.

        Args:
            message: Mensaje a loggear.
            **kwargs: Metadatos adicionales.
        """
        pass

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """
        Log a nivel INFO.

        Args:
            message: Mensaje a loggear.
            **kwargs: Metadatos adicionales.
        """
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """
        Log a nivel WARNING.

        Args:
            message: Mensaje a loggear.
            **kwargs: Metadatos adicionales.
        """
        pass

    @abstractmethod
    def error(
        self, message: str, exception: Optional[Exception] = None, **kwargs: Any
    ) -> None:
        """
        Log a nivel ERROR.

        Args:
            message: Mensaje a loggear.
            exception: Excepción asociada.
            **kwargs: Metadatos adicionales.
        """
        pass

    @abstractmethod
    def critical(
        self, message: str, exception: Optional[Exception] = None, **kwargs: Any
    ) -> None:
        """
        Log a nivel CRITICAL.

        Args:
            message: Mensaje a loggear.
            exception: Excepción asociada.
            **kwargs: Metadatos adicionales.
        """
        pass
