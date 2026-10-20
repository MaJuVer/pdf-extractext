from unittest.mock import MagicMock
from uuid import uuid4

from src.application.services.obtener_registro_service import ObtenerRegistroService
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


def test_obtener_registro_existente() -> None:
    fake_id = uuid4()
    registro_simulado = RegistroProcesamiento(
        id=fake_id,
        nombre_archivo_original="archivo.pdf",
        contenido_extraido="Texto de Prueba",
        hash_contenido="abc123hash",
    )

    mock_repository = MagicMock(spec=RegistroProcesamientoRepository)
    mock_repository.get_by_id.return_value = registro_simulado

    service = ObtenerRegistroService(mock_repository)
    resultado = service.ejecutar(str(fake_id))

    assert resultado is not None
    assert resultado.id == fake_id
    assert resultado.nombre_archivo_original == "archivo.pdf"
    mock_repository.get_by_id.assert_called_once_with(str(fake_id))
