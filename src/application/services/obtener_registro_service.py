from typing import Optional

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class ObtenerRegistroService:
    """Obtiene un registro de procesamiento por su ID."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository

    def ejecutar(self, id_registro: str) -> Optional[RegistroProcesamiento]:
        return self._repository.get_by_id(id_registro)
