"""Tests para get_by_hash en RegistroProcesamientoMongoRepositoryImpl."""

from mongomock import MongoClient

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.infrastructure.persistence.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoMongoRepositoryImpl,
)


def _repo() -> RegistroProcesamientoMongoRepositoryImpl:
    return RegistroProcesamientoMongoRepositoryImpl(
        db=MongoClient()["test_db"],
        collection_name="registros",
        entity_class=RegistroProcesamiento,
    )


def test_get_by_hash_existente() -> None:
    """Debe encontrar el registro por su hash."""
    repo = _repo()
    hash_contenido = "abc123" * 8

    entidad = RegistroProcesamiento(
        nombre_archivo_original="documento.pdf",
        contenido_extraido="Texto extraído",
        hash_contenido=hash_contenido,
    )
    repo.add(entidad)

    resultado = repo.get_by_hash(hash_contenido)

    assert resultado is not None
    assert resultado.nombre_archivo_original == "documento.pdf"
    assert resultado.hash_contenido == hash_contenido


def test_get_by_hash_inexistente() -> None:
    """Debe devolver None cuando no existe el hash."""
    assert _repo().get_by_hash("hash_inexistente") is None
