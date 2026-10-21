"""
Factory de dependencias para los servicios de RegistroProcesamiento.
"""

from src.application.services.actualizar_registro_service import (
    ActualizarRegistroService,
)
from src.application.services.eliminar_registro_service import EliminarRegistroService
from src.application.services.listar_registros_service import ListarRegistrosService
from src.application.services.obtener_por_hash_service import ObtenerPorHashService
from src.application.services.obtener_registro_service import ObtenerRegistroService
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
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


def get_listar_registros_service() -> ListarRegistrosService:
    """Factory para ListarRegistrosService."""
    return ListarRegistrosService(repository=get_registro_repository())


def get_obtener_por_hash_service() -> ObtenerPorHashService:
    """Factory para ObtenerPorHashService."""
    return ObtenerPorHashService(repository=get_registro_repository())
