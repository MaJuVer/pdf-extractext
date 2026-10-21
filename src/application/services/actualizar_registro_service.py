from typing import Optional

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class ActualizarRegistroService:
    """Actualiza los campos editables de un registro de procesamiento."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository

    def ejecutar(
        self,
        id_registro: str,
        nuevo_texto: str | None = None,
        nuevo_hash: str | None = None,
        nuevo_nombre_archivo: str | None = None,
    ) -> Optional[RegistroProcesamiento]:
        registro = self._repository.get_by_id(id_registro)

        if registro is None:
            return None

        if nuevo_texto is not None:
            registro.contenido_extraido = nuevo_texto
        if nuevo_hash is not None:
            registro.hash_contenido = nuevo_hash
        if nuevo_nombre_archivo is not None:
            registro.nombre_archivo_original = nuevo_nombre_archivo

        return self._repository.update(registro)
