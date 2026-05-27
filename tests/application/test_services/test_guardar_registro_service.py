"""
Tests para GuardarRegistroService con verificación de duplicados.

Este módulo valida que GuardarRegistroService verifique correctamente
si un documento ya existe por su hash antes de guardar.
"""

from unittest.mock import MagicMock

import pytest

from src.application.dtos.pdf_dtos import TextoExtraidoDTO
from src.application.services.guardar_registro_service import GuardarRegistroService
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.exceptions.domain_exception import DocumentoDuplicadoException


class TestGuardarRegistroServiceDuplicados:
    """Tests para verificación de documentos duplicados."""

    def test_documento_no_existente_se_guarda_correctamente(self) -> None:
        """
        Dado un PDF nuevo (hash no existe), debe guardar exitosamente.
        """
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
            hash_contenido=pdf.calcular_hash_sha256(),
        )

        mock_repo = MagicMock()
        mock_repo.find_by_hash.return_value = None
        mock_repo.add.return_value = entidad_simulada

        service = GuardarRegistroService(repository=mock_repo)

        resultado = service.ejecutar(pdf, texto_dto)

        mock_repo.find_by_hash.assert_called_once_with(pdf.calcular_hash_sha256())
        mock_repo.add.assert_called_once()

        assert resultado.id_registro is not None
        assert resultado.nombre_archivo_original == pdf.nombre_archivo

    def test_documento_duplicado_lanza_excepcion(self) -> None:
        """
        Dado un PDF duplicado (hash ya existe), debe lanzar DocumentoDuplicadoException.
        """
        contenido_pdf = b"%PDF-1.4 contenido duplicado"

        pdf = DocumentoPDF(
            nombre_archivo="duplicado.pdf",
            peso_bytes=len(contenido_pdf),
            contenido_binario=contenido_pdf,
        )

        texto_dto = TextoExtraidoDTO(
            contenido="Texto duplicado",
            cantidad_caracteres=17,
            cantidad_palabras=3,
        )

        registro_existente = RegistroProcesamiento(
            nombre_archivo_original="otro.pdf",
            contenido_extraido="Texto existente",
            hash_contenido=pdf.calcular_hash_sha256(),
        )

        mock_repo = MagicMock()
        mock_repo.find_by_hash.return_value = registro_existente

        service = GuardarRegistroService(repository=mock_repo)

        with pytest.raises(DocumentoDuplicadoException) as exc_info:
            service.ejecutar(pdf, texto_dto)

        mock_repo.find_by_hash.assert_called_once_with(pdf.calcular_hash_sha256())
        mock_repo.add.assert_not_called()

        assert exc_info.value.hash_contenido == pdf.calcular_hash_sha256()
        assert "ya existe" in str(exc_info.value)
