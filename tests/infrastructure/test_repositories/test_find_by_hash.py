"""Tests para find_by_hash en RegistroProcesamientoMongoRepositoryImpl."""

from mongomock import MongoClient

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.infrastructure.persistence.repositories.registro_procesamiento_repository import RegistroProcesamientoMongoRepositoryImpl


def test_find_by_hash_existente():
    """Debe encontrar el registro por su hash."""
    mock_client = MongoClient()
    db = mock_client["test_db"]

    repo = RegistroProcesamientoMongoRepositoryImpl(
        db=db, collection_name="registros", entity_class=RegistroProcesamiento
    )

    entidad = RegistroProcesamiento(
        nombre_archivo_original="documento.pdf",
        contenido_extraido="Texto extraído",
        hash_contenido="abc123" * 8,  # 64 caracteres simulando hash sha256
    )

    repo.add(entidad)

    resultado = repo.find_by_hash("abc123" * 8)

    assert resultado is not None
    assert resultado.nombre_archivo_original == "documento.pdf"
    assert resultado.hash_contenido == "abc123" * 8


def test_find_by_hash_inexistente():
    """Debe devolver None cuando no existe el hash."""
    mock_client = MongoClient()
    db = mock_client["test_db"]

    repo = RegistroProcesamientoMongoRepositoryImpl(
        db=db, collection_name="registros", entity_class=RegistroProcesamiento
    )

    resultado = repo.find_by_hash("hash_inexistente")

    assert resultado is None
