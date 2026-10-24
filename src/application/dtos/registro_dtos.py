"""DTOs para los casos de uso del CRUD de registros."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class RegistroDetalleDTO:
    """Vista de un registro de procesamiento para la frontera de interface."""

    id: UUID
    nombre_archivo_original: str
    contenido_extraido: str
    hash_contenido: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class RegistrosPaginadosDTO:
    """Resultado paginado de registros de procesamiento."""

    items: list[RegistroDetalleDTO]
    total: int
    page: int
    page_size: int
