from dataclasses import FrozenInstanceError

import pytest

from src.application.dtos.pdf_dtos import TextoExtraidoDTO


def test_texto_extraido_dto_es_inmutable() -> None:
    dto = TextoExtraidoDTO(contenido="Texto original del PDF", cantidad_caracteres=30, cantidad_palabras=5)

    with pytest.raises(FrozenInstanceError):
        dto.contenido = "Texto modificado maliciosamente"  # type: ignore[misc]
