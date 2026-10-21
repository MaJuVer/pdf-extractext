"""
Configuración de base de datos MongoDB.

El cliente se crea de forma perezosa para que importar la capa de
infraestructura no exija variables de entorno (facilita los tests).
"""

from functools import lru_cache
from typing import Generator

from pymongo import MongoClient
from pymongo.database import Database

from src.infrastructure.config.settings import get_settings


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    """Devuelve el cliente MongoDB compartido (singleton perezoso)."""
    return MongoClient(get_settings().DATABASE_URL)


def get_db() -> Generator[Database, None, None]:
    """Genera la conexión a la base de datos MongoDB."""
    yield get_client().get_database(get_settings().MONGO_DB)


def close_client() -> None:
    """Cierra el cliente compartido, si fue creado."""
    if get_client.cache_info().currsize:
        get_client().close()
        get_client.cache_clear()
