from unittest.mock import Mock
from uuid import uuid4
from src.application.services.eliminar_registro_service import EliminarRegistroService

def test_eliminar_registro_existente():
    # ARRANGE
    # Creamos un ID falso de prueba
    fake_id = uuid4()
    
    # Creamos nuestro repositorio falso
    mock_repository = Mock()
    
    # Le decimos al mock que cuando le pidan eliminar, devuelva True (simulando éxito)
    mock_repository.eliminar_por_id.return_value = True
    
    # Instanciamos el servicio (que todavía no existe) inyectándole el mock
    service = EliminarRegistroService(mock_repository)

    # ACT
    # Mandamos a ejecutar la eliminación
    resultado = service.ejecutar(fake_id)

    # ASSERT
    # Verificamos que el servicio nos devuelva True
    assert resultado is True
    # Verificamos que el servicio realmente haya llamado al método del repositorio con el ID correcto
    mock_repository.eliminar_por_id.assert_called_once_with(fake_id)