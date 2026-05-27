import pytest

from src.application.dtos.pdf_dtos import TextoExtraidoDTO


def test_texto_extraido_dto_es_inmutable():
    dto = TextoExtraidoDTO(
        contenido="Texto original del PDF", cantidad_caracteres=30, cantidad_palabras=5
    )

    with pytest.raises(Exception) as error_info:
        dto.contenido = "Texto modificado maliciosamente"

    print(f"\nEl error capturado fue: {error_info.type}")
