"""
Interfaz de repositorio para RegistroProcesamiento.

Define el contrato específico para la persistencia de registros
procesamiento, incluyendo la capacidad de buscar por hash SHA256
de contenido.
"""

from abc import abstractmethod
from typing import Optional

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.base_repository import BaseRepository


class RegistroProcesamientoRepository(BaseRepository[RegistroProcesamiento]):
    """
    Interface de repositorio para RegistroProcesamiento.

    Extiende BaseRepository con operaciones específicas del dominio
    relacionadas con la detección de documentos duplicados.
    """

    @abstractmethod
    def find_by_hash(self, hash_contenido: str) -> Optional[RegistroProcesamiento]:
        """
        Busca un registro por su hash SHA256 de contenido.

        Args:
            hash_contenido: Hash SHA256 del contenido del PDF.

        Returns:
            RegistroProcesamiento si existe, None en caso contrario.
        """
        raise NotImplementedError("Debe implementarse en la infraestructura")
