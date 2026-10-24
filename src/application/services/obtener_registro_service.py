from typing import Optional

from src.application.dtos.registro_dtos import RegistroDetalleDTO
from src.application.mappers.registro_procesamiento_mapper import (
    RegistroProcesamientoMapper,
)
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class ObtenerRegistroService:
    """Obtiene un registro de procesamiento por su ID."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository
        self._mapper = RegistroProcesamientoMapper()

    def ejecutar(self, id_registro: str) -> Optional[RegistroDetalleDTO]:
        registro = self._repository.get_by_id(id_registro)
        if registro is None:
            return None
        return self._mapper.to_detalle_dto(registro)
