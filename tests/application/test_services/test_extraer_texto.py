import pytest
from src.application.dtos.pdf_dtos import TextoExtraidoDTO
from src.application.interfaces.pdf_extractor_interface import PDFExtractorInterface
from src.application.services.extraer_texto import ExtraerTexto
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.exceptions.pdf_exceptions import DocumentoSinTextoException

class FakeExtractor(PDFExtractorInterface):
    def __init__(self, texto_a_retornar: str = ""):
        self._texto = texto_a_retornar
    
    def extract_text(self, contenido: bytes) -> str:
        return self._texto
    
class FakeExtractorVacio(PDFExtractorInterface):
    """Simula un extractor que devuelve texto vacío."""
    
    def extract_text(self, contenido: bytes) -> str:
        return ""
    

# TEST 1
def test_extraer_texto_devuelve_dto_con_texto():
    extractor = FakeExtractor()
    caso = ExtraerTexto(extractor=extractor)
    
    contenido = b"%PDF fake"
    pdf = DocumentoPDF(
        nombre_archivo="doc.pdf",
        peso_bytes=len(contenido),   
        contenido_binario=contenido
    )
    
    resultado = caso.execute(pdf)
    
    assert resultado.contenido == "Hola mundo PDF"


# TEST 2
def test_pdf_sin_texto_lanza_excepcion():
    extractor = FakeExtractorVacio()
    caso = ExtraerTexto(extractor=extractor)
    
    contenido = b"%PDF vacio"
    pdf = DocumentoPDF(
        nombre_archivo="vacio.pdf",
        peso_bytes=len(contenido),
        contenido_binario=contenido
    )
    
    with pytest.raises(DocumentoSinTextoException) as exc_info:
        caso.execute(pdf)
    
    assert "no contiene texto" in str(exc_info.value).lower()