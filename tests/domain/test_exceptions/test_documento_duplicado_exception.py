import pytest

from src.domain.exceptions.domain_exception import DocumentoDuplicadoException


class TestDocumentoDuplicadoException:
    """Tests para DocumentoDuplicadoException."""

    def test_documento_duplicado_default(self) -> None:
        """Debe crear la excepción con mensaje y código por defecto."""
        with pytest.raises(DocumentoDuplicadoException) as exc_info:
            raise DocumentoDuplicadoException()

        assert "ya existe" in str(exc_info.value)
        assert exc_info.value.code == "DOCUMENTO_DUPLICADO"

    def test_documento_duplicado_custom(self) -> None:
        """Debe permitir un mensaje personalizado."""
        with pytest.raises(DocumentoDuplicadoException) as exc_info:
            raise DocumentoDuplicadoException("El hash XYZ ya existe")

        assert "XYZ" in str(exc_info.value)
        assert exc_info.value.code == "DOCUMENTO_DUPLICADO"

    def test_documento_duplicado_hash(self) -> None:
        """Debe almacenar el hash del documento duplicado."""
        hash_prueba = "abc123"

        with pytest.raises(DocumentoDuplicadoException) as exc_info:
            raise DocumentoDuplicadoException(hash_contenido=hash_prueba)

        assert exc_info.value.hash_contenido == hash_prueba
        assert "abc123" in str(exc_info.value)
