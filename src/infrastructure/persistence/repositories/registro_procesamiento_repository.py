"""
Implementación de RegistroProcesamientoRepository en MongoDB.
"""

from typing import Optional

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)
from src.infrastructure.persistence.repositories.base_repository_impl import (
    BaseMongoRepositoryImpl,
)


class RegistroProcesamientoMongoRepositoryImpl(
    BaseMongoRepositoryImpl[RegistroProcesamiento],
    RegistroProcesamientoRepository,
):
    """
    Implementación MongoDB de RegistroProcesamientoRepository.

    Extende BaseMongoRepositoryImpl con la capacidad de buscar
    registros por hash SHA256 de contenido.
    """

    def get_by_hash(self, hash_contenido: str) -> Optional[RegistroProcesamiento]:
        """
        Obtiene un registro por su hash SHA256 de contenido.

        Args:
            hash_contenido: Hash SHA256 del contenido del PDF.

        Returns:
            RegistroProcesamiento si existe, None en caso contrario.
        """
        doc = self._collection.find_one({"hash_contenido": hash_contenido})
        return self._doc_to_entity(doc)

    def find_by_hash(self, hash_contenido: str) -> Optional[RegistroProcesamiento]:
        """
        Alias de get_by_hash para compatibilidad.

        Args:
            hash_contenido: Hash SHA256 del contenido del PDF.

        Returns:
            RegistroProcesamiento si existe, None en caso contrario.
        """
        return self.get_by_hash(hash_contenido)
