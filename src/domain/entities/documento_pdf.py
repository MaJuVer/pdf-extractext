"""
Entidad DocumentoPDF del dominio.

Representa un archivo PDF válido que ha pasado las restricciones del negocio.
Esta entidad es pura y no conoce detalles de persistencia ni frameworks web.
"""

import hashlib
from dataclasses import dataclass
from pathlib import Path

from src.domain.entities.base_entity import BaseEntity


@dataclass(kw_only=True)
class DocumentoPDF(BaseEntity):
    """
    Representa un documento PDF validado en el sistema.

    Attributes:
        nombre_archivo: Nombre completo del archivo (ej: "documento.pdf").
        peso_bytes: Tamaño del archivo en bytes.
        contenido_binario: Contenido raw del archivo en formato bytes.

    Example:
        >>> pdf = DocumentoPDF(
        ...     nombre_archivo="factura.pdf",
        ...     peso_bytes=1024,
        ...     contenido_binario=b"%PDF-1.4..."
        ... )
        >>> pdf.es_extension_valida()
        True
    """

    nombre_archivo: str
    peso_bytes: int
    contenido_binario: bytes

    def __post_init__(self) -> None:
        """Validaciones de integridad post-inicialización."""
        if not self.nombre_archivo:
            raise ValueError("El nombre del archivo no puede estar vacío")
        if self.peso_bytes < 0:
            raise ValueError("El peso en bytes no puede ser negativo")
        if self.peso_bytes != len(self.contenido_binario):
            raise ValueError(
                "El peso_bytes no coincide con el tamaño real del contenido"
            )

    def es_extension_valida(self) -> bool:
        """
        Verifica si el archivo tiene extensión .pdf (case-insensitive).

        Returns:
            True si la extensión es .pdf, False en caso contrario.
        """
        return Path(self.nombre_archivo).suffix.lower() == ".pdf"

    def tienen_contenidos_identicos(self, otro: "DocumentoPDF") -> bool:
        """
        Verifica si dos documentos tienen el mismo hash SHA256.

        Args:
            otro: Otro documento PDF para comparar.

        Returns:
            True si los hashes SHA256 coinciden, False en caso contrario.
        """
        return self.calcular_hash_sha256() == otro.calcular_hash_sha256()

    def calcular_hash_sha256(self) -> str:
        """
        Calcula el hash SHA256 del contenido binario del PDF.

        Returns:
            Representacion hexadecimal del hash SHA256 del contenido.
        """
        hasher = hashlib.sha256()
        hasher.update(self.contenido_binario)
        return hasher.hexdigest()

    def tiene_contenido(self) -> bool:
        """
        Verifica si el archivo tiene contenido (peso > 0).

        Returns:
            True si el archivo tiene al menos 1 byte.
        """
        return self.peso_bytes > 0
