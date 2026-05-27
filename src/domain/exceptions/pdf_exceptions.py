"""
Excepciones específicas para el procesamiento de PDFs.
"""
from src.domain.exceptions.domain_exception import DomainException

class PDFExtractionException(DomainException):
    """
    Error al extraer texto de un PDF.
    
    Se lanza cuando la librería externa no puede procesar el archivo
    (corrupto, encriptado, formato inválido).
    """
    
    def __init__(self, message: str) -> None:
        super().__init__(message, code="PDF_EXTRACTION_ERROR")
        
class DocumentoSinTextoException(DomainException):
    """
    El PDF no contiene texto extraíble.
    
    Se lanza cuando el PDF es válido pero solo contiene imágenes
    o páginas en blanco.
    """
    
    def __init__(self, nombre_archivo: str) -> None:
        message = f"El documento '{nombre_archivo}' no contiene texto extraíble"
        super().__init__(message, code="PDF_NO_TEXT")