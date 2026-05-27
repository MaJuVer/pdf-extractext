"""
DTOs para el flujo de procesamiento de archivos PDF.

Estos DTOs transportan datos entre la capa de interface y los casos de uso,
garantizando que la capa de aplicación no dependa de frameworks externos.
"""

import uuid
from dataclasses import dataclass, field
from io import BytesIO

from src.application.dtos.base_dto import BaseInputDTO


@dataclass(frozen=True)
class ArchivoEntradaDTO(BaseInputDTO):
    """
    DTO para recibir un archivo desde la capa de interface.

    Attributes:
        nombre: Nombre completo del archivo (ej: "documento.pdf").
        contenido: Contenido binario del archivo en bytes.
        extension: Extensión del archivo sin punto (ej: "pdf", "txt").

    Note:
        Este DTO se construye en el router a partir del UploadFile de FastAPI,
        pero la capa de aplicación solo conoce este DTO puro.

    Example:
        >>> dto = ArchivoEntradaDTO(
        ...     nombre="factura.pdf",
        ...     contenido=b"%PDF-1.4...",
        ...     extension="pdf"
        ... )
    """

    nombre: str
    contenido: bytes
    extension: str


@dataclass(frozen=True)
class TextoExtraidoDTO:
    """
    DTO para transportar el texto extraído de un PDF.

    Attributes:
        contenido: Texto plano extraído del documento.
        cantidad_caracteres: Cantidad de caracteres del texto extraído.
        cantidad_palabras: Cantidad aproximada de palabras en el texto.

    Example:
        >>> dto = TextoExtraidoDTO(
        ...     contenido="Este es el texto extraído del PDF",
        ...     cantidad_caracteres=36,
        ...     cantidad_palabras=7
        ... )
    """

    contenido: str
    cantidad_caracteres: int
    cantidad_palabras: int


@dataclass(frozen=True)
class ArchivoSalidaDTO:
    """
    DTO para entregar un archivo generado a la capa de interface.

    Attributes:
        nombre: Nombre del archivo a devolver al cliente.
        buffer: Buffer en memoria con el contenido del archivo.
        content_type: Tipo MIME del archivo (ej: "text/plain").

    Note:
        El buffer es un BytesIO que permite al router de FastAPI
        enviar el archivo como respuesta sin escribir en disco.

    Example:
        >>> buffer = BytesIO(b"Contenido del archivo")
        >>> dto = ArchivoSalidaDTO(
        ...     nombre="resultado.txt",
        ...     buffer=buffer,
        ...     content_type="text/plain; charset=utf-8"
        ... )
    """

    nombre: str
    buffer: BytesIO
    content_type: str = "text/plain; charset=utf-8"


@dataclass(frozen=True, kw_only=True)
class RegistroProcesamientoOutputDTO:
    """
    DTO para devolver información del registro guardado en base de datos.

    Attributes:
        id_registro: UUID del registro creado.
        nombre_archivo_original: Nombre original del archivo procesado.
        longitud_texto: Cantidad de caracteres extraídos.
        mensaje_confirmacion: Mensaje descriptivo del éxito de la operación.

    Example:
        >>> dto = RegistroProcesamientoOutputDTO(
        ...     id_registro=uuid4(),
        ...     nombre_archivo_original="documento.pdf",
        ...     longitud_texto=1500,
        ...     mensaje_confirmacion="Archivo procesado y registrado exitosamente"
        ... )
    """

    id_registro: str = field(default_factory=lambda: str(uuid.uuid4()))
    nombre_archivo_original: str
    longitud_texto: int
    mensaje_confirmacion: str = "Archivo procesado exitosamente"
