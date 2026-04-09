"""
Rutas de health check.

Provee endpoints para verificar el estado de la aplicación.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    """
    Respuesta de health check.

    Attributes:
        status: Estado de la aplicación ("healthy" o "unhealthy").
        timestamp: Timestamp ISO de la respuesta.
        version: Versión de la aplicación.
    """

    status: str
    timestamp: str
    version: str


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Verifica que la aplicación esté funcionando correctamente.",
)
async def health_check() -> HealthResponse:
    """
    Endpoint de health check.

    Returns:
        HealthResponse con estado de la aplicación.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
        version="0.1.0",
    )


@router.get(
    "/ready",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness check",
    description="Verifica que la aplicación esté lista para recibir tráfico.",
)
async def readiness_check() -> HealthResponse:
    """
    Endpoint de readiness check.

    Returns:
        HealthResponse indicando si la app está lista.
    """
    return HealthResponse(
        status="ready",
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
        version="0.1.0",
    )
