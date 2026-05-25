from io import BytesIO
from pypdf import PdfReader
from src.application.interfaces.pdf_extractor_interface import PDFExtractorInterface
from src.domain.exceptions.pdf_exceptions import PDFExtractionException

class PyPDFExtractor(PDFExtractorInterface):
    def extract_text(self, contenido_binario: bytes) -> str:
        try:
            reader = PdfReader(BytesIO(contenido_binario))
            paginas = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(paginas)
        except Exception as e:
            raise PDFExtractionException(f"Error al procesar PDF: {str(e)}") from e