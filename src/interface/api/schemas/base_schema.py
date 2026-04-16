"""
Schemas base para la API.

Define schemas Pydantic comunes que pueden ser extendidos
por schemas específicos de recursos.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Schema base con configuración común.

    Configura:
    - Strict mode para validación estricta
    - Extra=forbid para rechazar campos extra
    """

    model_config = ConfigDict(
        strict=True,
        extra="forbid",
        populate_by_name=True,
    )


class BaseResponseSchema(BaseSchema):
    """
    Schema base para respuestas.

    Incluye campos comunes de auditoría.

    Attributes:
        id: Identificador único UUID.
        created_at: Fecha de creación ISO8601.
        updated_at: Fecha de última actualización ISO8601.
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
            }
        }
    )


class BaseListResponse(BaseSchema):
    """
    Schema base para respuestas de listas paginadas.

    Attributes:
        items: Lista de items.
        total: Total de items disponibles.
        page: Página actual.
        page_size: Tamaño de página.
    """

    items: list
    total: int
    page: int
    page_size: int


class ErrorResponse(BaseSchema):
    """
    Schema para respuestas de error.

    Attributes:
        error: Tipo de error.
        message: Descripción del error.
        code: Código de error opcional.
    """

    error: str
    message: str
    code: Optional[str] = None
