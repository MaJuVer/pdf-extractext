"""Tests de la creación de índices de MongoDB."""

import logging
from unittest.mock import MagicMock

import pytest
from mongomock import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError

from src.infrastructure.persistence.indexes import HASH_INDEX_NAME, ensure_indexes


def test_ensure_indexes_crea_indice_unico_sobre_hash_contenido() -> None:
    db = MongoClient()["test_db"]

    ensure_indexes(db)

    indice = db["registros"].index_information()[HASH_INDEX_NAME]
    assert indice["key"] == [("hash_contenido", 1)]
    assert indice["unique"] is True


def test_ensure_indexes_es_idempotente() -> None:
    db = MongoClient()["test_db"]

    ensure_indexes(db)
    ensure_indexes(db)

    assert HASH_INDEX_NAME in db["registros"].index_information()


def test_ensure_indexes_loguea_y_relanza_pymongo_error(
    caplog: pytest.LogCaptureFixture,
) -> None:
    db = MagicMock(spec=Database)
    db.__getitem__.return_value.create_index.side_effect = PyMongoError("fallo")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(PyMongoError):
            ensure_indexes(db)

    assert "hash_contenido" in caplog.text
