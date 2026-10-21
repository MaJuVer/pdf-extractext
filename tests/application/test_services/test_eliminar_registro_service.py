from unittest.mock import MagicMock
from uuid import uuid4

from src.application.services.eliminar_registro_service import EliminarRegistroService
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


def test_eliminar_registro_existente() -> None:
    fake_id = str(uuid4())

    mock_repository = MagicMock(spec=RegistroProcesamientoRepository)
    mock_repository.delete.return_value = True

    service = EliminarRegistroService(mock_repository)
    resultado = service.ejecutar(fake_id)

    assert resultado is True
    mock_repository.delete.assert_called_once_with(fake_id)
