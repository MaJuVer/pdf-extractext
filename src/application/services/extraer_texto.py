from src.application.dtos.pdf_dtos import TextoExtraidoDTO
from src.application.interfaces.pdf_extractor_interface import PDFExtractorInterface
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.exceptions.pdf_exceptions import DocumentoSinTextoException


class ExtraerTexto:
    def __init__(self, extractor: PDFExtractorInterface) -> None:
        self._extractor = extractor
    
    def execute(self, documento: DocumentoPDF) -> TextoExtraidoDTO:
        texto = self._extractor.extract_text(documento.contenido_binario)
        
        if not texto or not texto.strip():
            raise DocumentoSinTextoException(documento.nombre_archivo)
        
        palabras = texto.split()
        
        return TextoExtraidoDTO(
            contenido=texto,
            cantidad_caracteres=len(texto),
            cantidad_palabras=len(palabras),
        )
