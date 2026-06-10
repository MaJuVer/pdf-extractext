from unittest.mock import Mock
import pytest 
from uuid import uuid4


from src.domain.exceptions.domain_exception import ValidationException
from src.application.services.obtener_registro_service import ObtenerRegistroService
from src.domain.entities.registro_procesamiento import RegistroProcesamiento

def test_obtener_registro_existente(): 
    #Arrange 
    #ID falso y registro de prueba simulando contenidos en BD 
    fake_id = uuid4()
    registro_simulado= RegistroProcesamiento(
        id= fake_id,
        nombre_archivo_original="archivo.pdf" , 
        contenido_extraido = "Texto de Prueba",
        hash_contenido = "abc123hash"
    )

    mock_repository=Mock()

    mock_repository.get_by_id.return_value = registro_simulado

    service= ObtenerRegistroService(mock_repository)

    resultado_dto = service.ejecutar(fake_id)
    
    # ASSERT (Verificar que todo salió como queríamos)
    # Comprobamos que el servicio nos devuelva los datos correctos del registro
    assert resultado_dto is not None
    assert resultado_dto.id == fake_id
    assert resultado_dto.nombre_archivo_original == "archivo.pdf"
# Verificamos que el servicio efectivamente haya llamado al repositorio con el ID correcto
    mock_repository.get_by_id.assert_called_once_with(fake_id)