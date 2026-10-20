"""Mapeo de entidades de dominio a schemas de respuesta HTTP."""

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.interface.api.schemas.registro_schema import RegistroProcesamientoResponse


def to_response(registro: RegistroProcesamiento) -> RegistroProcesamientoResponse:
    """Convierte una entidad RegistroProcesamiento a su schema de respuesta."""
    return RegistroProcesamientoResponse(
        id=registro.id,
        nombre_archivo_original=registro.nombre_archivo_original,
        contenido_extraido=registro.contenido_extraido,
        hash_contenido=registro.hash_contenido,
        created_at=registro.created_at,
        updated_at=registro.updated_at,
    )
