import pytest

from src.application.dtos.pdf_dtos import ArchivoEntradaDTO
from src.application.services.pdf_validator import verificar_restricciones
from src.domain.exceptions.domain_exception import ValidationException

MAX_SIZE = 1024
MIN_SIZE = 1


def _dto(extension: str = "pdf", contenido: bytes = b"%PDF-1.4 contenido") -> ArchivoEntradaDTO:
    return ArchivoEntradaDTO(
        nombre=f"documento.{extension}",
        contenido=contenido,
        extension=extension,
    )


def test_rechaza_archivo_que_no_sea_pdf() -> None:
    with pytest.raises(ValidationException):
        verificar_restricciones(_dto(extension="txt"), MAX_SIZE, MIN_SIZE)


def test_archivo_valido_pdf() -> None:
    verificar_restricciones(_dto(), MAX_SIZE, MIN_SIZE)


def test_archivo_grande_rechazado() -> None:
    dto_invalido = _dto(contenido=b"A" * MAX_SIZE)

    with pytest.raises(ValidationException):
        verificar_restricciones(dto_invalido, MAX_SIZE, MIN_SIZE)


def test_archivo_vacio_rechazado() -> None:
    dto_invalido = _dto(contenido=b"")

    with pytest.raises(ValidationException):
        verificar_restricciones(dto_invalido, MAX_SIZE, MIN_SIZE)
