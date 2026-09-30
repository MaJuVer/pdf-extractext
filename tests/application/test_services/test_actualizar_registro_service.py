from unittest.mock import Mock
from uuid import uuid4
from src.application.services.actualizar_registro_service import ActualizarRegistroService
from src.domain.entities.registro_procesamiento import RegistroProcesamiento

def test_actualizar_registro_existente():
    # ARRANGE
    fake_id = uuid4()
    
    # Este es el registro "viejo" que simula estar en la base de datos
    registro_existente = RegistroProcesamiento(
        id=fake_id,
        nombre_archivo_original="documento.pdf",
        contenido_extraido="Texto viejo y aburrido",
        hash_contenido="hash_viejo"
    )
    
    mock_repository = Mock()
    # Programamos al mock: cuando busquen por ID, devolvé el registro viejo
    mock_repository.get_by_id.return_value = registro_existente
    mock_repository.update.return_value = registro_existente

    # Instanciamos nuestro futuro servicio
    service = ActualizarRegistroService(mock_repository)

    # ACT
    # Le pasamos el ID y los nuevos datos que queremos pisar
    resultado = service.ejecutar(
        id_registro=fake_id,
        nuevo_texto="Texto nuevo y mejorado",
        nuevo_hash="hash_nuevo_123"
    )

    # ASSERT
    # Comprobamos que el objeto devuelto tenga los datos actualizados
    assert resultado.contenido_extraido == "Texto nuevo y mejorado"
    assert resultado.hash_contenido == "hash_nuevo_123"
    
    # Verificamos que el servicio haya llamado al repositorio para guardar la actualización
    mock_repository.update.assert_called_once_with(resultado)