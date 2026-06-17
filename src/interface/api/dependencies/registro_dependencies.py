"""
Factory de dependencias para los servicios de RegistroProcesamiento.
"""

from src.application.services.actualizar_registro_service import ActualizarRegistroService
from src.application.services.eliminar_registro_service import EliminarRegistroService
from src.application.services.obtener_registro_service import ObtenerRegistroService
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.base_repository import BaseRepository
from src.infrastructure.persistence.database import get_db
from src.infrastructure.persistence.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoMongoRepositoryImpl,
)


def get_registro_repository() -> RegistroProcesamientoMongoRepositoryImpl:
    """
    Factory que crea una instancia del repositorio de registros.

    Returns:
        RegistroProcesamientoMongoRepositoryImpl: Repositorio configurado.
    """
    db = next(get_db())
    return RegistroProcesamientoMongoRepositoryImpl(
        db=db,
        collection_name="registros",
        entity_class=RegistroProcesamiento,
    )


def get_obtener_registro_service() -> ObtenerRegistroService:
    """Factory para ObtenerRegistroService."""
    return ObtenerRegistroService(repository=get_registro_repository())


def get_actualizar_registro_service() -> ActualizarRegistroService:
    """Factory para ActualizarRegistroService."""
    return ActualizarRegistroService(repository=get_registro_repository())


def get_eliminar_registro_service() -> EliminarRegistroService:
    """Factory para EliminarRegistroService."""
    return EliminarRegistroService(repository=get_registro_repository())


def get_base_repository() -> BaseRepository[RegistroProcesamiento]:
    """Factory para obtener el repositorio base (usado directamente en listado)."""
    return get_registro_repository()