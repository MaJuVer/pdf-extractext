"""Tests de integración HTTP para POST /pdf/process."""

from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from src.application.dtos.pdf_dtos import ArchivoEntradaDTO, ArchivoSalidaDTO, ProcesarPdfOutputDTO
from src.domain.exceptions.domain_exception import (
    DocumentoDuplicadoException,
    ValidationException,
)
from src.domain.exceptions.pdf_exceptions import (
    DocumentoSinTextoException,
    PDFExtractionException,
    PDFInvalidException,
)
from src.interface.api.dependencies.pdf_dependencies import get_pdf_orchestrator
from src.interface.main import app

client = TestClient(app)


class FakeOrchestrator:
    """Orquestador de prueba que devuelve un TXT o lanza un error fijo."""

    def __init__(self, error: Exception | None = None) -> None:
        self._error = error

    def execute(self, archivo_dto: ArchivoEntradaDTO) -> ProcesarPdfOutputDTO:
        if self._error is not None:
            raise self._error
        return ProcesarPdfOutputDTO(
            archivo_salida=ArchivoSalidaDTO(
                nombre="documento.txt",
                buffer=BytesIO(b"texto extraido"),
            ),
            registro=None,
            fue_cacheado=False,
        )


def _override(error: Exception | None = None) -> None:
    app.dependency_overrides[get_pdf_orchestrator] = lambda: FakeOrchestrator(error)


@pytest.fixture(autouse=True)
def _limpiar_overrides() -> None:
    yield
    app.dependency_overrides.clear()


def _pdf(nombre: str = "documento.pdf") -> dict[str, tuple[str, bytes, str]]:
    return {"file": (nombre, b"%PDF-1.4 contenido", "application/pdf")}


def test_procesar_pdf_exitoso() -> None:
    _override()

    response = client.post("/pdf/process", files=_pdf())

    assert response.status_code == 200
    assert response.content == b"texto extraido"
    assert response.headers["content-type"].startswith("text/plain")
    assert "documento.txt" in response.headers["content-disposition"]


def test_rechaza_content_type_no_pdf() -> None:
    _override()

    response = client.post(
        "/pdf/process",
        files={"file": ("documento.txt", b"texto", "text/plain")},
    )

    assert response.status_code == 400


def test_pdf_invalido_devuelve_422() -> None:
    _override(PDFInvalidException("falso.pdf"))

    response = client.post("/pdf/process", files=_pdf("falso.pdf"))

    assert response.status_code == 422


def test_pdf_sin_texto_devuelve_422() -> None:
    _override(DocumentoSinTextoException("vacio.pdf"))

    response = client.post("/pdf/process", files=_pdf("vacio.pdf"))

    assert response.status_code == 422


def test_duplicado_devuelve_409() -> None:
    _override(DocumentoDuplicadoException(hash_contenido="hash"))

    response = client.post("/pdf/process", files=_pdf())

    assert response.status_code == 409


def test_error_de_extraccion_devuelve_500() -> None:
    _override(PDFExtractionException("fallo"))

    response = client.post("/pdf/process", files=_pdf())

    assert response.status_code == 500


def test_restriccion_incumplida_devuelve_400() -> None:
    _override(ValidationException("El archivo es demasiado grande"))

    response = client.post("/pdf/process", files=_pdf())

    assert response.status_code == 400
