from datetime import datetime, timezone
from uuid import uuid4

from src.application.dtos.registro_dtos import RegistroDetalleDTO
from src.application.mappers.registro_procesamiento_mapper import (
    RegistroProcesamientoMapper,
)
from src.domain.entities.registro_procesamiento import RegistroProcesamiento


def test_to_detalle_dto_transpone_todos_los_campos() -> None:
    creado = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    actualizado = datetime(2026, 1, 3, 4, 5, 6, tzinfo=timezone.utc)
    entidad = RegistroProcesamiento(
        id=uuid4(),
        nombre_archivo_original="documento.pdf",
        contenido_extraido="Texto extraído",
        hash_contenido="a" * 64,
        created_at=creado,
        updated_at=actualizado,
    )

    dto = RegistroProcesamientoMapper().to_detalle_dto(entidad)

    assert isinstance(dto, RegistroDetalleDTO)
    assert dto.id == entidad.id
    assert dto.nombre_archivo_original == "documento.pdf"
    assert dto.contenido_extraido == "Texto extraído"
    assert dto.hash_contenido == "a" * 64
    assert dto.created_at == creado
    assert dto.updated_at == actualizado
