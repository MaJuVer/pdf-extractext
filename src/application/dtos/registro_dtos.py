"""DTOs para los casos de uso del CRUD de registros."""

from dataclasses import dataclass

from src.domain.entities.registro_procesamiento import RegistroProcesamiento


@dataclass(frozen=True)
class RegistrosPaginadosDTO:
    """Resultado paginado de registros de procesamiento."""

    items: list[RegistroProcesamiento]
    total: int
    page: int
    page_size: int
