"""
Creación de índices de MongoDB.

La creación de índices es una responsabilidad de persistencia, no de
la capa web. El composition root solo invoca esta función al arrancar.
"""

import logging

from pymongo import ASCENDING
from pymongo.database import Database
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)

HASH_INDEX_NAME = "uq_hash_contenido"


def ensure_indexes(db: Database) -> None:
    """
    Garantiza el índice único sobre `hash_contenido`.

    Raises:
        PyMongoError: Si el índice no puede crearse (por ejemplo, porque
            ya existen duplicados en la colección).
    """
    try:
        db["registros"].create_index(
            [("hash_contenido", ASCENDING)],
            unique=True,
            name=HASH_INDEX_NAME,
        )
    except PyMongoError:
        logger.exception("No se pudo crear el indice unico de hash_contenido")
        raise
