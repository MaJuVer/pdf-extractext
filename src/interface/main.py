"""
Punto de entrada principal de la aplicación FastAPI.

Configura la aplicación FastAPI con:
- Ciclo de vida de la base de datos (índices y cierre del cliente)
- Routers de la API
- Configuración de CORS
- Documentación automática

Siguiendo los principios de Clean Architecture, este archivo
permanece en la capa más externa (Interface) y no contiene
lógica de negocio, solo configuración de la aplicación web.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config.settings import Settings, get_settings
from src.infrastructure.persistence.database import close_client, get_db
from src.infrastructure.persistence.indexes import ensure_indexes
from src.interface.api.routes.health import router as health_router
from src.interface.api.routes.pdf import router as pdf_router
from src.interface.api.routes.registro_routes import router as registro_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Prepara la base de datos al arrancar y cierra el cliente al salir."""
    db_generator = get_db()
    ensure_indexes(next(db_generator))
    try:
        yield
    finally:
        close_client()


def create_application() -> FastAPI:
    """
    Factory para crear y configurar la aplicación FastAPI.

    Returns:
        FastAPI: Instancia configurada de la aplicación.
    """
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    _configure_middleware(application, settings)
    _configure_routers(application)

    return application


def _configure_middleware(application: FastAPI, settings: Settings) -> None:
    """
    Configura middleware de la aplicación.

    Args:
        application: Instancia de FastAPI.
        settings: Configuración de la aplicación.
    """
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials="*" not in settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _configure_routers(application: FastAPI) -> None:
    """
    Registra los routers de la aplicación.

    Args:
        application: Instancia de FastAPI.
    """
    application.include_router(health_router, tags=["Health"])
    application.include_router(pdf_router, tags=["PDF"])
    application.include_router(registro_router, tags=["Registros"])


app = create_application()


def main() -> None:
    """Ejecuta la API con Uvicorn (entrypoint de `uv run run`)."""
    import uvicorn

    uvicorn.run("src.interface.main:app", host="0.0.0.0", port=8000)
