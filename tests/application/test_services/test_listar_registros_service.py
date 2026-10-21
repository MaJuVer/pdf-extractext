from unittest.mock import MagicMock

from src.application.services.listar_registros_service import ListarRegistrosService
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


def test_listar_delega_la_paginacion_al_repositorio() -> None:
    mock_repository = MagicMock(spec=RegistroProcesamientoRepository)
    mock_repository.get_paginated.return_value = ([], 25)
    service = ListarRegistrosService(mock_repository)

    resultado = service.ejecutar(page=3, page_size=10)

    mock_repository.get_paginated.assert_called_once_with(skip=20, limit=10)
    assert resultado.total == 25
    assert resultado.page == 3
    assert resultado.page_size == 10
