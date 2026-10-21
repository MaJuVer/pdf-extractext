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
        skip = (page - 1) * page_size
        items, total = self._repository.get_paginated(skip=skip, limit=page_size)

        return RegistrosPaginadosDTO(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
