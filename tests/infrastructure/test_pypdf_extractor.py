"""Tests del adaptador real de pypdf, con PDFs construidos en memoria."""

import pytest

from src.domain.exceptions.pdf_exceptions import PDFExtractionException
from src.infrastructure.external_services.pypdf_extractor import PyPDFExtractor


def _pdf_minimo(texto: str | None) -> bytes:
    """Construye un PDF válido de una página, con o sin texto."""
    stream = f"BT /F1 24 Tf 72 700 Td ({texto}) Tj ET".encode() if texto else b""
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    salida = bytearray(b"%PDF-1.4\n")
    offsets = []
    for numero, objeto in enumerate(objetos, 1):
        offsets.append(len(salida))
        salida += b"%d 0 obj\n" % numero + objeto + b"\nendobj\n"
    xref = len(salida)
    salida += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objetos) + 1)
    for offset in offsets:
        salida += b"%010d 00000 n \n" % offset
    salida += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objetos) + 1,
        xref,
    )
    return bytes(salida)


def test_extract_text_extrae_el_texto_del_pdf() -> None:
    assert PyPDFExtractor().extract_text(_pdf_minimo("Hola mundo")).strip() == "Hola mundo"


def test_extract_text_devuelve_vacio_si_el_pdf_no_tiene_texto() -> None:
    assert PyPDFExtractor().extract_text(_pdf_minimo(None)).strip() == ""


def test_extract_text_lanza_excepcion_con_pdf_corrupto() -> None:
    with pytest.raises(PDFExtractionException):
        PyPDFExtractor().extract_text(b"%PDF-1.4\nbasura\n" * 3)
