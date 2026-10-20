"""Caso de uso: listar registros de procesamiento con paginación."""

from src.application.dtos.registro_dtos import RegistrosPaginadosDTO
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class ListarRegistrosService:
    """Lista registros aplicando paginación."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository

    def ejecutar(self, page: int, page_size: int) -> RegistrosPaginadosDTO:
        """
        Devuelve una página de registros.

        Args:
            page: Número de página (1-indexado).
            page_size: Cantidad de items por página.

        Returns:
            RegistrosPaginadosDTO con los items y el total disponible.
        """
        all_registros = self._repository.get_all()
        skip = (page - 1) * page_size
        items = all_registros[skip : skip + page_size]

        return RegistrosPaginadosDTO(
            items=items,
            total=len(all_registros),
            page=page,
            page_size=page_size,
        )
