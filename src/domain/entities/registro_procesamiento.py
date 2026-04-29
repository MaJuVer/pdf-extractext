"""
Entidad RegistroProcesamiento del dominio.

Representa el registro histórico de un archivo PDF que fue procesado exitosamente.
Esta entidad justifica el uso de una base de datos documental (MongoDB).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.entities.base_entity import BaseEntity


@dataclass
class RegistroProcesamiento(BaseEntity):
    """
    Representa un registro histórico de procesamiento de PDF.

    Attributes:
        id_registro: Identificador único del registro (UUID).
        nombre_archivo_original: Nombre original del archivo procesado.
        contenido_extraido: Texto extraído del PDF en formato string.
        fecha_procesamiento: Timestamp exacto del procesamiento.

    Example:
        >>> from src.domain.entities.documento_pdf import DocumentoPDF
        >>> pdf = DocumentoPDF(
        ...     nombre_archivo="documento.pdf",
        ...     peso_bytes=1024,
        ...     contenido_binario=b"%PDF-1.4..."
        ... )
        >>> registro = RegistroProcesamiento(
        ...     nombre_archivo_original=pdf.nombre_archivo,
        ...     contenido_extraido="Texto extraído del PDF...",
        ... )
        >>> registro.id_registro  # UUID generado automáticamente
    """

    nombre_archivo_original: str
    contenido_extraido: str
    id_registro: UUID = field(default_factory=uuid4)
    fecha_procesamiento: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        """Validaciones de integridad post-inicialización."""
        if not self.nombre_archivo_original:
            raise ValueError("El nombre del archivo original no puede estar vacío")

    def resumen(self) -> str:
        """
        Genera un resumen del procesamiento para logs o debugging.

        Returns:
            String con información resumida del registro.
        """
        longitud_texto = len(self.contenido_extraido)
        return (
            f"Registro[{self.id_registro}]: "
            f"'{self.nombre_archivo_original}' "
            f"({longitud_texto} caracteres extraídos)"
        )

    def longitud_contenido(self) -> int:
        """
        Retorna la cantidad de caracteres del texto extraído.

        Returns:
            Número entero con la longitud del contenido.
        """
        return len(self.contenido_extraido)
