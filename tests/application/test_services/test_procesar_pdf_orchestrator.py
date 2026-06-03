"""
Tests para ProcesarPdfOrchestrator.

Estos tests definen el comportamiento esperado del orquestador
que coordina el flujo completo de procesamiento de PDF.
"""

from io import BytesIO
from unittest.mock import MagicMock

import pytest

from src.application.dtos.pdf_dtos import (
    ArchivoEntradaDTO,
    ArchivoSalidaDTO,
    ProcesarPdfOutputDTO,
    RegistroProcesamientoOutputDTO,
    TextoExtraidoDTO,
)
from src.application.interfaces.pdf_extractor_interface import PDFExtractorInterface
from src.application.services.procesar_pdf_orchestrator import ProcesarPdfOrchestrator
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.exceptions.domain_exception import DocumentoDuplicadoException, ValidationException
from src.domain.exceptions.pdf_exceptions import DocumentoSinTextoException, PDFInvalidException
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class TestProcesarPdfOrchestrator:
    """Tests para el orquestador de procesamiento de PDF."""

    def test_documento_nuevo_procesa_y_guarda(self) -> None:
        """
        Dado un PDF nuevo (hash no existe), debe extraer texto,
        guardar registro y generar archivo.
        """
        contenido_pdf = b"%PDF-1.4 " + b"x" * 100
        archivo_dto = ArchivoEntradaDTO(
            nombre="documento.pdf",
            contenido=contenido_pdf,
            extension="pdf",
        )
        texto_extraido = "Texto extraído del PDF"

        mock_extractor = MagicMock(spec=PDFExtractorInterface)
        mock_extractor.extract_text.return_value = texto_extraido

        mock_repo = MagicMock(spec=RegistroProcesamientoRepository)
        mock_repo.get_by_hash.return_value = None
        mock_repo.find_by_hash.return_value = None
        entidad_guardada = RegistroProcesamiento(
            nombre_archivo_original="documento.pdf",
            contenido_extraido=texto_extraido,
            hash_contenido="hash_fake_123",
        )
        mock_repo.add.return_value = entidad_guardada

        orchestrator = ProcesarPdfOrchestrator(
            extractor=mock_extractor,
            repository=mock_repo,
        )

        resultado = orchestrator.execute(archivo_dto)

        assert isinstance(resultado, ProcesarPdfOutputDTO)
        assert resultado.fue_cacheado is False
        assert resultado.registro is not None
        mock_extractor.extract_text.assert_called_once()
        mock_repo.add.assert_called_once()

    def test_documento_duplicado_retorna_cacheado(self) -> None:
        """
        Dado un PDF duplicado (hash ya existe), debe recuperar
        texto de BD sin guardar nuevo registro.
        """
        contenido_pdf = b"%PDF-1.4 " + b"y" * 100
        archivo_dto = ArchivoEntradaDTO(
            nombre="duplicado.pdf",
            contenido=contenido_pdf,
            extension="pdf",
        )
        texto_cacheado = "Texto previamente extraído"

        mock_extractor = MagicMock(spec=PDFExtractorInterface)

        registro_existente = MagicMock(spec=RegistroProcesamiento)
        registro_existente.contenido_extraido = texto_cacheado

        mock_repo = MagicMock(spec=RegistroProcesamientoRepository)
        mock_repo.get_by_hash.return_value = registro_existente

        orchestrator = ProcesarPdfOrchestrator(
            extractor=mock_extractor,
            repository=mock_repo,
        )

        resultado = orchestrator.execute(archivo_dto)

        assert isinstance(resultado, ProcesarPdfOutputDTO)
        assert resultado.fue_cacheado is True
        assert resultado.registro is None
        mock_extractor.extract_text.assert_not_called()
        mock_repo.add.assert_not_called()

    def test_validacion_falla_con_archivo_no_pdf(self) -> None:
        """
        Archivo sin extension PDF debe lanzar ValidationException.
        """
        contenido = b"no es un pdf"
        archivo_dto = ArchivoEntradaDTO(
            nombre="documento.txt",
            contenido=contenido,
            extension="txt",
        )

        mock_extractor = MagicMock(spec=PDFExtractorInterface)
        mock_repo = MagicMock(spec=RegistroProcesamientoRepository)

        orchestrator = ProcesarPdfOrchestrator(
            extractor=mock_extractor,
            repository=mock_repo,
        )

        with pytest.raises(ValidationException):
            orchestrator.execute(archivo_dto)

    def test_validacion_falla_por_magic_bytes_invalidos(self) -> None:
        """
        Archivo con contenido que no es PDF valido
        debe lanzar PDFInvalidException.
        """
        contenido = b"NO_ES_PDF" + b"x" * 95
        archivo_dto = ArchivoEntradaDTO(
            nombre="falso.pdf",
            contenido=contenido,
            extension="pdf",
        )

        mock_extractor = MagicMock(spec=PDFExtractorInterface)
        mock_repo = MagicMock(spec=RegistroProcesamientoRepository)

        orchestrator = ProcesarPdfOrchestrator(
            extractor=mock_extractor,
            repository=mock_repo,
        )

        with pytest.raises(PDFInvalidException):
            orchestrator.execute(archivo_dto)

    def test_extraccion_falla_por_pdf_sin_texto(self) -> None:
        """
        PDF sin texto extraible debe lanzar DocumentoSinTextoException.
        """
        contenido_pdf = b"%PDF-1.4 " + b"z" * 100
        archivo_dto = ArchivoEntradaDTO(
            nombre="vacio.pdf",
            contenido=contenido_pdf,
            extension="pdf",
        )

        mock_extractor = MagicMock(spec=PDFExtractorInterface)
        mock_extractor.extract_text.return_value = ""

        mock_repo = MagicMock(spec=RegistroProcesamientoRepository)
        mock_repo.get_by_hash.return_value = None

        orchestrator = ProcesarPdfOrchestrator(
            extractor=mock_extractor,
            repository=mock_repo,
        )

        with pytest.raises(DocumentoSinTextoException):
            orchestrator.execute(archivo_dto)

    def test_documento_duplicado_genera_archivo_correcto(self) -> None:
        """
        Verifica que el archivo generado para duplicado
        tenga el contenido correcto del cache.
        """
        contenido_pdf = b"%PDF-1.4 " + b"w" * 100
        archivo_dto = ArchivoEntradaDTO(
            nombre="original.pdf",
            contenido=contenido_pdf,
            extension="pdf",
        )
        texto_cacheado = "Contenido guardado previamente"

        mock_repo = MagicMock(spec=RegistroProcesamientoRepository)
        registro_existente = MagicMock(spec=RegistroProcesamiento)
        registro_existente.contenido_extraido = texto_cacheado
        mock_repo.get_by_hash.return_value = registro_existente

        orchestrator = ProcesarPdfOrchestrator(
            extractor=MagicMock(),
            repository=mock_repo,
        )

        resultado = orchestrator.execute(archivo_dto)

        buffer = resultado.archivo_salida.buffer
        buffer.seek(0)
        assert buffer.read().decode("utf-8") == texto_cacheado
        assert resultado.archivo_salida.nombre == "original.txt"


class TestProcesarPdfOutputDTO:
    """Tests para el DTO de salida del orquestador."""

    def test_dto_es_inmutable(self) -> None:
        """El DTO debe ser inmutable (frozen=True)."""
        archivo = ArchivoSalidaDTO(
            nombre="test.txt",
            buffer=BytesIO(b"contenido"),
            content_type="text/plain",
        )
        registro = RegistroProcesamientoOutputDTO(
            id_registro="123",
            nombre_archivo_original="test.pdf",
            longitud_texto=100,
        )

        dto = ProcesarPdfOutputDTO(
            archivo_salida=archivo,
            registro=registro,
            fue_cacheado=False,
        )

        with pytest.raises(AttributeError):
            dto.fue_cacheado = True