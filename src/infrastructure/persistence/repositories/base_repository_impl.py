"""
Implementación base de repositorio.

Implementa la interfaz BaseRepository usando MongoDB.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar, cast
from uuid import UUID

from pymongo.database import Database

from src.domain.entities.base_entity import BaseEntity
from src.domain.repositories.base_repository import BaseRepository

T = TypeVar("T", bound=BaseEntity)


class BaseMongoRepositoryImpl(BaseRepository[T], Generic[T]):
    """
    Implementación base de repositorio con MongoDB.
    """

    def __init__(
        self, db: Database, collection_name: str, entity_class: Type[T]
    ) -> None:
        """
        Inicializa el repositorio.

        Args:
            db: Base de datos de PyMongo.
            collection_name: Nombre de la colección (ej: "usuarios").
            entity_class: Clase de la entidad a manejar.
        """
        self._collection = db[collection_name]
        self._entity_class = entity_class

    def _doc_to_entity(self, doc: dict[str, Any] | None) -> Optional[T]:
        """Traduce un documento de Mongo a una Entidad de Dominio."""
        if not doc:
            return None
        doc["id"] = UUID(doc.pop("_id"))
        return self._entity_class(**doc)

    def _entity_to_doc(self, entity: T) -> dict[str, Any]:
        """Traduce una Entidad de Dominio a un documento de Mongo."""
        doc = (
            entity.model_dump()
            if hasattr(entity, "model_dump")
            else entity.__dict__.copy()
        )
        doc["_id"] = str(doc.pop("id"))
        return doc

    def get_by_id(self, entity_id: str) -> Optional[T]:
        try:
            uuid_id = UUID(entity_id)
            doc = self._collection.find_one({"_id": str(uuid_id)})
            return self._doc_to_entity(doc)
        except ValueError:
            return None

    def get_all(self) -> List[T]:
        docs = self._collection.find()
        return [cast(T, self._doc_to_entity(doc)) for doc in docs if doc]

    def add(self, entity: T) -> T:
        doc = self._entity_to_doc(entity)
        self._collection.insert_one(doc)
        return entity

    def update(self, entity: T) -> T:
        if hasattr(entity, "update_timestamp"):
            entity.update_timestamp()

        doc = self._entity_to_doc(entity)
        entity_id = doc.pop("_id")

        self._collection.update_one({"_id": entity_id}, {"$set": doc})
        return entity

    def delete(self, entity_id: str) -> bool:
        try:
            uuid_id = UUID(entity_id)
            result = self._collection.delete_one({"_id": str(uuid_id)})
            return result.deleted_count > 0
        except ValueError:
            return False

    def exists(self, entity_id: str) -> bool:
        return self.get_by_id(entity_id) is not None
