"""
Schemas para el endpoint de procesamiento de PDF.

Define los schemas de request/response para el endpoint
POST /pdf/process usando FastAPI UploadFile.
"""

from src.interface.api.schemas.base_schema import BaseSchema


class PDFProcessResponse(BaseSchema):
    """
    Schema de respuesta metadata del procesamiento PDF.

    Attributes:
        nombre_archivo: Nombre del archivo PDF procesado.
        fue_cacheado: Indica si el resultado vino de cache.
        mensaje: Mensaje descriptivo del resultado.
    """

    nombre_archivo: str
    fue_cacheado: bool
    mensaje: str