"""
DTOs para el flujo de procesamiento de archivos PDF.

Estos DTOs transportan datos entre la capa de interface y los casos de uso,
garantizando que la capa de aplicación no dependa de frameworks externos.
"""

from dataclasses import dataclass
from io import BytesIO
from typing import Optional

from src.application.dtos.base_dto import BaseInputDTO, BaseOutputDTO


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
        >>> dto.es_pdf()
        True
    """

    nombre: str
    contenido: bytes
    extension: str

    def __post_init__(self) -> None:
        """Validaciones de integridad post-inicialización."""
        object.__setattr__(self, "nombre", self.nombre.strip())
        object.__setattr__(self, "extension", self.extension.lower().strip())

        if not self.nombre:
            raise ValueError("El nombre del archivo no puede estar vacío")
        if not self.extension:
            raise ValueError("La extensión del archivo no puede estar vacía")
        if not self.contenido:
            raise ValueError("El contenido del archivo no puede estar vacío")

    def es_pdf(self) -> bool:
        """
        Verifica si el archivo tiene extensión PDF.

        Returns:
            True si la extensión es 'pdf', False en caso contrario.
        """
        return self.extension == "pdf"

    def peso_en_bytes(self) -> int:
        """
        Retorna el tamaño del archivo en bytes.

        Returns:
            Número entero representando el tamaño.
        """
        return len(self.contenido)


@dataclass(frozen=True)
class TextoExtraidoDTO(BaseOutputDTO):
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

    def __post_init__(self) -> None:
        """Validaciones de integridad post-inicialización."""
        if self.cantidad_caracteres < 0:
            raise ValueError("La cantidad de caracteres no puede ser negativa")
        if self.cantidad_palabras < 0:
            raise ValueError("La cantidad de palabras no puede ser negativa")

    def esta_vacio(self) -> bool:
        """
        Verifica si el texto extraído está vacío.

        Returns:
            True si no hay contenido, False en caso contrario.
        """
        return self.cantidad_caracteres == 0

    def preview(self, longitud: int = 100) -> str:
        """
        Genera una vista previa del texto truncado.

        Args:
            longitud: Cantidad máxima de caracteres a mostrar.

        Returns:
            String con el inicio del texto, truncado si es necesario.
        """
        if len(self.contenido) <= longitud:
            return self.contenido
        return self.contenido[:longitud] + "..."


@dataclass(frozen=True)
class ArchivoSalidaDTO(BaseOutputDTO):
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

    def __post_init__(self) -> None:
        """Validaciones de integridad post-inicialización."""
        if not self.nombre:
            raise ValueError("El nombre del archivo no puede estar vacío")

    def peso_en_bytes(self) -> int:
        """
        Retorna el tamaño del buffer en bytes.

        Returns:
            Número entero representando el tamaño del archivo.
        """
        return self.buffer.getbuffer().nbytes

    def obtener_bytes(self) -> bytes:
        """
        Obtiene el contenido del buffer como bytes.

        Returns:
            Contenido del archivo en formato bytes.
        """
        posicion_actual = self.buffer.tell()
        self.buffer.seek(0)
        contenido = self.buffer.read()
        self.buffer.seek(posicion_actual)
        return contenido


@dataclass(frozen=True)
class RegistroProcesamientoOutputDTO(BaseOutputDTO):
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

    id_registro: str
    nombre_archivo_original: str
    longitud_texto: int
    mensaje_confirmacion: str = "Archivo procesado exitosamente"

    def __post_init__(self) -> None:
        """Validaciones de integridad post-inicialización."""
        if not self.id_registro:
            raise ValueError("El ID del registro no puede estar vacío")
        if not self.nombre_archivo_original:
            raise ValueError("El nombre del archivo original no puede estar vacío")
        if self.longitud_texto < 0:
            raise ValueError("La longitud del texto no puede ser negativa")
