"""
Tests para BaseEntity.

Verifica comportamiento de entidades base:
- Generación automática de ID
- Timestamps de auditoría
- Igualdad basada en identidad
"""

from datetime import datetime, timezone
from uuid import UUID

from src.domain.entities.base_entity import BaseEntity


def test_entity_generates_uuid():
    """Las entidades generan automáticamente un UUID."""
    entity = BaseEntity()
    assert isinstance(entity.id, UUID)


def test_entity_timestamps_on_creation():
    """Las entidades tienen timestamps al crearse."""
    before = datetime.now(timezone.utc)
    entity = BaseEntity()
    after = datetime.now(timezone.utc)

    assert before <= entity.created_at <= after
    assert before <= entity.updated_at <= after


def test_entities_equal_if_same_id():
    """Dos entidades son iguales si tienen el mismo ID."""
    id = UUID("550e8400-e29b-41d4-a716-446655440000")
    entity1 = BaseEntity(id=id)
    entity2 = BaseEntity(id=id)

    assert entity1 == entity2


def test_entities_not_equal_if_different_id():
    """Dos entidades son diferentes si tienen IDs distintos."""
    entity1 = BaseEntity()
    entity2 = BaseEntity()

    assert entity1 != entity2


def test_entity_update_timestamp():
    """update_timestamp modifica el updated_at."""
    entity = BaseEntity()
    original_updated_at = entity.updated_at

    entity.update_timestamp()

    assert entity.updated_at > original_updated_at
