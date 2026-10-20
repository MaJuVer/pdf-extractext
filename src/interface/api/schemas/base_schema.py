"""
Schemas base para la API.

Define schema Pydantic común que puede ser extendido por schemas
específicos de recursos.
"""

from typing import Optional

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
