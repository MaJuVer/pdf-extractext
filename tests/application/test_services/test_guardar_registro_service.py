from unittest.mock import MagicMock

from src.application.dtos.pdf_dtos import TextoExtraidoDTO
from src.application.services.guardar_registro_service import GuardarRegistroService
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.entities.registro_procesamiento import RegistroProcesamiento


def test_service_guarda_registro_y_retorna_output_dto():
    contenido_pdf = b"%PDF-1.4 contenido de prueba"

    pdf = DocumentoPDF(
        nombre_archivo="prueba.pdf",
        peso_bytes=len(contenido_pdf),
        contenido_binario=contenido_pdf,
    )

    texto_dto = TextoExtraidoDTO(
        contenido="Texto extraído de prueba",
        cantidad_caracteres=27,
        cantidad_palabras=5,
    )

    entidad_simulada = RegistroProcesamiento(
        nombre_archivo_original=pdf.nombre_archivo,
        contenido_extraido=texto_dto.contenido,
    )

    mock_repo = MagicMock()
    mock_repo.add.return_value = entidad_simulada

    service = GuardarRegistroService(repository=mock_repo)

    resultado = service.ejecutar(pdf, texto_dto)

    mock_repo.add.assert_called_once()
    entidad_guardada = mock_repo.add.call_args[0][0]
    assert entidad_guardada.nombre_archivo_original == pdf.nombre_archivo
    assert entidad_guardada.contenido_extraido == texto_dto.contenido

    assert resultado.id_registro is not None
    assert resultado.nombre_archivo_original == pdf.nombre_archivo
    assert resultado.longitud_texto == len(texto_dto.contenido)
    assert resultado.mensaje_confirmacion == "Archivo procesado exitosamente"
