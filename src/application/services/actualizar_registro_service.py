from typing import Optional

from src.application.dtos.registro_dtos import RegistroDetalleDTO
from src.application.mappers.registro_procesamiento_mapper import (
    RegistroProcesamientoMapper,
)
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class ActualizarRegistroService:
    """Actualiza los campos editables de un registro de procesamiento."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository
        self._mapper = RegistroProcesamientoMapper()

    def ejecutar(
        self,
        id_registro: str,
        nuevo_texto: str | None = None,
        nuevo_nombre_archivo: str | None = None,
    ) -> Optional[RegistroDetalleDTO]:
        registro = self._repository.get_by_id(id_registro)

        if registro is None:
            return None

        if nuevo_texto is not None:
            registro.contenido_extraido = nuevo_texto
        if nuevo_nombre_archivo is not None:
            registro.nombre_archivo_original = nuevo_nombre_archivo

        actualizado = self._repository.update(registro)
        return self._mapper.to_detalle_dto(actualizado)
