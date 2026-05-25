import hashlib

from src.domain.entities.documento_pdf import DocumentoPDF


class TestDocumentoPDFHash:
    """Tests para el cálculo de hash SHA256 en DocumentoPDF."""

    def test_calcular_hash_sha256(self) -> None:
        """Debe calcular correctamente el hash SHA256 del contenido binario."""
        contenido = b"contenido de prueba para hashing"
        pdf = DocumentoPDF(
            nombre_archivo="documento.pdf",
            peso_bytes=len(contenido),
            contenido_binario=contenido,
        )

        hash_esperado = hashlib.sha256(contenido).hexdigest()

        assert pdf.calcular_hash_sha256() == hash_esperado

    def test_calcular_hash_sha256_dos_veces(self) -> None:
        """Debe devolver el mismo hash al calcularlo dos veces."""
        contenido = b"contenido consistente"
        pdf = DocumentoPDF(
            nombre_archivo="documento.pdf",
            peso_bytes=len(contenido),
            contenido_binario=contenido,
        )

        hash_1 = pdf.calcular_hash_sha256()
        hash_2 = pdf.calcular_hash_sha256()

        assert hash_1 == hash_2

    def test_calcular_hash_sha256_contenidos_distintos(self) -> None:
        """Dos contenidos distintos deben generar hashes distintos."""
        contenido_a = b"contenido A"
        contenido_b = b"contenido B"

        pdf_a = DocumentoPDF(
            nombre_archivo="a.pdf",
            peso_bytes=len(contenido_a),
            contenido_binario=contenido_a,
        )
        pdf_b = DocumentoPDF(
            nombre_archivo="b.pdf",
            peso_bytes=len(contenido_b),
            contenido_binario=contenido_b,
        )

        assert pdf_a.calcular_hash_sha256() != pdf_b.calcular_hash_sha256()
