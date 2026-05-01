from src.application.dtos.pdf_dtos import TextoExtraidoDTO
from src.application.services.generar_archivo_txt import GenerarArchivoTxtUseCase


def test_generar_archivo_txt_devuelve_buffer_con_contenido():
    dto_entrada = TextoExtraidoDTO(
        contenido="Hola mundo", cantidad_caracteres=10, cantidad_palabras=2
    )
    nombre_original = "documento.pdf"

    caso_uso = GenerarArchivoTxtUseCase()
    resultado = caso_uso.execute(dto_entrada, nombre_original)

    assert resultado.nombre == "documento.txt"
    assert resultado.content_type == "text/plain; charset=utf-8"

    buffer = resultado.buffer
    buffer.seek(0)
    assert buffer.read().decode("utf-8") == "Hola mundo"
