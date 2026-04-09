"""
Configuración de base de datos MongoDB.
"""

from typing import Generator

from pymongo import MongoClient
from pymongo.database import Database

from src.infrastructure.config.settings import get_settings

settings = get_settings()

client: MongoClient = MongoClient(settings.database_url)


def get_db() -> Generator[Database, None, None]:
    """
    Genera la conexión a la base de datos MongoDB.
    """
    db = client.get_database(settings.database_name)
    try:
        yield db
    finally:
        pass
