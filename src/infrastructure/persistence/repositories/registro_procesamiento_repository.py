from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.infrastructure.persistence.repositories.base_repository_impl import (
    BaseMongoRepositoryImpl,
)


class RegistroProcesamientoMongoRepositoryImpl(
    BaseMongoRepositoryImpl[RegistroProcesamiento]
):
    pass
