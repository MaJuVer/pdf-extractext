from unittest.mock import MagicMock
from uuid import uuid4

from src.application.services.actualizar_registro_service import (
    ActualizarRegistroService,
)
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


def test_actualizar_registro_existente() -> None:
    fake_id = uuid4()

    registro_existente = RegistroProcesamiento(
        id=fake_id,
        nombre_archivo_original="documento.pdf",
        contenido_extraido="Texto viejo y aburrido",
        hash_contenido="hash_viejo",
    )

    mock_repository = MagicMock(spec=RegistroProcesamientoRepository)
    mock_repository.get_by_id.return_value = registro_existente
    mock_repository.update.return_value = registro_existente

    service = ActualizarRegistroService(mock_repository)
    resultado = service.ejecutar(
        id_registro=str(fake_id),
        nuevo_texto="Texto nuevo y mejorado",
        nuevo_nombre_archivo="renombrado.pdf",
    )

    assert resultado is not None
    assert resultado.contenido_extraido == "Texto nuevo y mejorado"
    assert resultado.hash_contenido == "hash_viejo"
    assert resultado.nombre_archivo_original == "renombrado.pdf"
    mock_repository.update.assert_called_once_with(registro_existente)


def test_actualizar_registro_inexistente_devuelve_none() -> None:
    mock_repository = MagicMock(spec=RegistroProcesamientoRepository)
    mock_repository.get_by_id.return_value = None

    service = ActualizarRegistroService(mock_repository)

    assert service.ejecutar(id_registro=str(uuid4()), nuevo_texto="x") is None
    mock_repository.update.assert_not_called()
