from mongomock import MongoClient

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.infrastructure.persistence.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoMongoRepositoryImpl,
)


def test_mongo_repository_guarda_y_recupera_registro():
    mock_client = MongoClient()
    db = mock_client["test_db"]

    repo = RegistroProcesamientoMongoRepositoryImpl(
        db=db, collection_name="registros", entity_class=RegistroProcesamiento
    )

    entidad = RegistroProcesamiento(
        nombre_archivo_original="test.pdf", contenido_extraido="Texto extraido del PDF"
    )

    entidad_guardada = repo.add(entidad)
    entidad_recuperada = repo.get_by_id(str(entidad_guardada.id))

    assert entidad_recuperada is not None
    assert entidad_recuperada.nombre_archivo_original == entidad.nombre_archivo_original
    assert entidad_recuperada.contenido_extraido == entidad.contenido_extraido
