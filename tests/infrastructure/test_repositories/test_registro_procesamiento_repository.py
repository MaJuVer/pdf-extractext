from uuid import uuid4

import pytest
from mongomock import MongoClient
from pymongo import ASCENDING

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.exceptions.domain_exception import DocumentoDuplicadoException
from src.infrastructure.persistence.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoMongoRepositoryImpl,
)


def _repo() -> RegistroProcesamientoMongoRepositoryImpl:
    return RegistroProcesamientoMongoRepositoryImpl(
        db=MongoClient()["test_db"],
        collection_name="registros",
        entity_class=RegistroProcesamiento,
    )


def _registro(hash_contenido: str = "hash-1") -> RegistroProcesamiento:
    return RegistroProcesamiento(
        nombre_archivo_original="test.pdf",
        contenido_extraido="Texto extraido del PDF",
        hash_contenido=hash_contenido,
    )


def test_mongo_repository_guarda_y_recupera_registro() -> None:
    repo = _repo()
    entidad = _registro()

    entidad_guardada = repo.add(entidad)
    entidad_recuperada = repo.get_by_id(str(entidad_guardada.id))

    assert entidad_recuperada is not None
    assert entidad_recuperada.nombre_archivo_original == entidad.nombre_archivo_original
    assert entidad_recuperada.contenido_extraido == entidad.contenido_extraido


def test_update_modifica_el_registro() -> None:
    repo = _repo()
    entidad = repo.add(_registro())

    entidad.contenido_extraido = "Texto actualizado"
    repo.update(entidad)

    recuperada = repo.get_by_id(str(entidad.id))
    assert recuperada is not None
    assert recuperada.contenido_extraido == "Texto actualizado"


def test_delete_elimina_el_registro() -> None:
    repo = _repo()
    entidad = repo.add(_registro())

    assert repo.delete(str(entidad.id)) is True
    assert repo.get_by_id(str(entidad.id)) is None
    assert repo.delete(str(uuid4())) is False


def test_exists_indica_presencia() -> None:
    repo = _repo()
    entidad = repo.add(_registro())

    assert repo.exists(str(entidad.id)) is True
    assert repo.exists(str(uuid4())) is False


def test_get_paginated_devuelve_pagina_y_total() -> None:
    repo = _repo()
    for hash_contenido in ("hash-1", "hash-2", "hash-3"):
        repo.add(_registro(hash_contenido=hash_contenido))

    items, total = repo.get_paginated(skip=1, limit=1)

    assert total == 3
    assert len(items) == 1


def test_add_duplicado_traduce_duplicate_key() -> None:
    repo = _repo()
    repo._collection.create_index(  # type: ignore[attr-defined]
        [("hash_contenido", ASCENDING)], unique=True
    )
    repo.add(_registro(hash_contenido="hash-duplicado"))

    with pytest.raises(DocumentoDuplicadoException):
        repo.add(_registro(hash_contenido="hash-duplicado"))
