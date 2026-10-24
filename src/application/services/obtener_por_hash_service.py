"""Caso de uso: obtener un registro de procesamiento por hash."""

from typing import Optional

from src.application.dtos.registro_dtos import RegistroDetalleDTO
from src.application.mappers.registro_procesamiento_mapper import (
    RegistroProcesamientoMapper,
)
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class ObtenerPorHashService:
    """Obtiene un registro por su hash SHA256."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository
        self._mapper = RegistroProcesamientoMapper()

    def ejecutar(self, hash_contenido: str) -> Optional[RegistroDetalleDTO]:
        """Devuelve el registro asociado al hash, o None si no existe."""
        registro = self._repository.get_by_hash(hash_contenido)
        if registro is None:
            return None
        return self._mapper.to_detalle_dto(registro)
