"""
Schemas para el CRUD de RegistroProcesamiento.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import ConfigDict, Field, model_validator

from src.interface.api.schemas.base_schema import BaseSchema


class RegistroProcesamientoBase(BaseSchema):
    """Base schema con atributos comunes."""

    nombre_archivo_original: str = Field(..., min_length=1, max_length=255)
    contenido_extraido: str


class RegistroProcesamientoUpdate(BaseSchema):
    """Schema para actualizar un registro."""

    nombre_archivo_original: Optional[str] = Field(None, min_length=1, max_length=255)
    contenido_extraido: Optional[str] = None

    @model_validator(mode="after")
    def validar_al_menos_un_campo(self) -> "RegistroProcesamientoUpdate":
        """Exige al menos un campo para actualizar."""
        if self.nombre_archivo_original is None and self.contenido_extraido is None:
            raise ValueError("Debe proporcionar al menos un campo para actualizar.")
        return self


class RegistroProcesamientoResponse(BaseSchema):
    """Schema de respuesta para un registro."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nombre_archivo_original": "documento.pdf",
                "contenido_extraido": "Texto extraído del PDF...",
                "hash_contenido": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
            }
        },
    )

    id: UUID
    nombre_archivo_original: str
    contenido_extraido: str
    hash_contenido: str
    created_at: datetime
    updated_at: datetime


class RegistroListResponse(BaseSchema):
    """Schema para respuestas paginadas de registros."""

    items: list[RegistroProcesamientoResponse]
    total: int
    page: int
    page_size: int


class RegistroDeleteResponse(BaseSchema):
    """Schema para respuesta de eliminación."""

    eliminado: bool
    id_registro: str
    mensaje: str
