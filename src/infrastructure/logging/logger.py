"""
Implementación concreta del servicio de logging.

Implementa LoggerInterface usando la biblioteca estándar logging.
"""

import logging
import sys
from typing import Any, Optional

from src.application.interfaces.logger_interface import LoggerInterface


class Logger(LoggerInterface):
    """
    Implementación de logging usando el módulo estándar.

    Configura handlers para consola y formato estructurado.

    Attributes:
        _logger: Instancia del logger de Python.

    Example:
        >>> logger = Logger("my_app")
        >>> logger.info("Usuario creado", user_id="123")
    """

    def __init__(self, name: str, level: str = "INFO") -> None:
        """
        Inicializa el logger con configuración básica.

        Args:
            name: Nombre del logger.
            level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        if not self._logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Configura handlers para salida por consola."""
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def _format_extras(self, **kwargs: Any) -> str:
        """Formatea metadatos adicionales."""
        if not kwargs:
            return ""
        parts = [f"{k}={v}" for k, v in kwargs.items()]
        return " | " + " ".join(parts)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a nivel DEBUG."""
        self._logger.debug(message + self._format_extras(**kwargs))

    def info(self, message: str, **kwargs: Any) -> None:
        """Log a nivel INFO."""
        self._logger.info(message + self._format_extras(**kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a nivel WARNING."""
        self._logger.warning(message + self._format_extras(**kwargs))

    def error(
        self, message: str, exception: Optional[Exception] = None, **kwargs: Any
    ) -> None:
        """Log a nivel ERROR."""
        extras = self._format_extras(**kwargs)
        if exception:
            extras += f" | exception={type(exception).__name__}: {exception}"
        self._logger.error(message + extras)

    def critical(
        self, message: str, exception: Optional[Exception] = None, **kwargs: Any
    ) -> None:
        """Log a nivel CRITICAL."""
        extras = self._format_extras(**kwargs)
        if exception:
            extras += f" | exception={type(exception).__name__}: {exception}"
        self._logger.critical(message + extras)


def get_logger(name: str = "app") -> Logger:
    """
    Factory para obtener un logger configurado.

    Args:
        name: Nombre del logger.

    Returns:
        Logger: Instancia configurada.
    """
    return Logger(name)
