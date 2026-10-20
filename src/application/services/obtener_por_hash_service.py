"""Caso de uso: obtener un registro de procesamiento por hash."""

from typing import Optional

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class ObtenerPorHashService:
    """Obtiene un registro por su hash SHA256."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository

    def ejecutar(self, hash_contenido: str) -> Optional[RegistroProcesamiento]:
        """Devuelve el registro asociado al hash, o None si no existe."""
        return self._repository.get_by_hash(hash_contenido)
