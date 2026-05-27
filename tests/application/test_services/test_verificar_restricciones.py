import pytest

from src.application.dtos.pdf_dtos import ArchivoEntradaDTO 
from src.domain.exceptions.domain_exception import ValidationException
from src.application.services.pdf_validator import RestrictionVerifier

def test_rechaza_archivo_que_no_sea_pdf():
    #1 Arrange
    dto_invalido= ArchivoEntradaDTO(
        nombre="documento.txt",
        contenido=b"contenido falso"*10,
        extension="txt"
    )

    with pytest.raises(ValidationException):
        RestrictionVerifier(dto_invalido)

def test_archivo_valido_pdf():
    dto_valido = ArchivoEntradaDTO(
        nombre="documento.pdf",
        contenido=b"contenido falso"*10 ,
        extension= "pdf"
    )

    RestrictionVerifier(dto_valido)

def test_archivo_grande_rechazado():
    dto_invalido= ArchivoEntradaDTO(
        nombre="archivo_falso",
        contenido= b"A"*200000000 ,
        extension = "pdf"
    )
    with pytest.raises(ValidationException):
        RestrictionVerifier(dto_invalido)

def test_archivo_vacio():
    dto_invalido = ArchivoEntradaDTO(
        nombre= "archivo_vacio" , 
        contenido = b"",
        extension= "pdf" 
    )
    with pytest.raises(ValidationException):
        RestrictionVerifier(dto_invalido)