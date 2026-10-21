"""Tests para GuardarRegistroService."""

from unittest.mock import MagicMock

import pytest

from src.application.dtos.pdf_dtos import TextoExtraidoDTO
from src.application.services.guardar_registro_service import GuardarRegistroService
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.exceptions.domain_exception import DocumentoDuplicadoException
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


def _crear_pdf() -> DocumentoPDF:
    contenido_pdf = b"%PDF-1.4 contenido de prueba"
    return DocumentoPDF(
        nombre_archivo="prueba.pdf",
        peso_bytes=len(contenido_pdf),
        contenido_binario=contenido_pdf,
    )


def _crear_texto() -> TextoExtraidoDTO:
    return TextoExtraidoDTO(
        contenido="Texto extraído de prueba",
        cantidad_caracteres=27,
        cantidad_palabras=5,
    )


def test_documento_se_guarda_con_el_hash_provisto() -> None:
    pdf = _crear_pdf()
    texto_dto = _crear_texto()
    hash_contenido = pdf.calcular_hash_sha256()

    entidad_simulada = RegistroProcesamiento(
        nombre_archivo_original=pdf.nombre_archivo,
        contenido_extraido=texto_dto.contenido,
        hash_contenido=hash_contenido,
    )

    mock_repo = MagicMock(spec=RegistroProcesamientoRepository)
    mock_repo.add.return_value = entidad_simulada

    service = GuardarRegistroService(repository=mock_repo)
    resultado = service.ejecutar(pdf, texto_dto, hash_contenido)

    entidad_persistida = mock_repo.add.call_args.args[0]
    assert entidad_persistida.hash_contenido == hash_contenido
    assert resultado.id_registro is not None
    assert resultado.nombre_archivo_original == pdf.nombre_archivo


def test_error_de_duplicado_del_repositorio_se_propaga() -> None:
    pdf = _crear_pdf()
    texto_dto = _crear_texto()

    mock_repo = MagicMock(spec=RegistroProcesamientoRepository)
    mock_repo.add.side_effect = DocumentoDuplicadoException(hash_contenido=pdf.calcular_hash_sha256())

    service = GuardarRegistroService(repository=mock_repo)

    with pytest.raises(DocumentoDuplicadoException):
        service.ejecutar(pdf, texto_dto, pdf.calcular_hash_sha256())
