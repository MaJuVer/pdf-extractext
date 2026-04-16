"""
Punto de entrada principal de la aplicación FastAPI.

Configura la aplicación FastAPI con:
- Middleware de manejo de errores
- Routers de la API
- Configuración de CORS
- Documentación automática

Siguiendo los principios de Clean Architecture, este archivo
permanece en la capa más externa (Interface) y no contiene
lógica de negocio, solo configuración de la aplicación web.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config.settings import Settings
from src.interface.api.routes import health


def create_application() -> FastAPI:
    """
    Factory para crear y configurar la aplicación FastAPI.

    Returns:
        FastAPI: Instancia configurada de la aplicación.
    """
    settings = Settings()

    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
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
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _configure_routers(application: FastAPI) -> None:
    """
    Registra los routers de la aplicación.

    Args:
        application: Instancia de FastAPI.
    """
    application.include_router(health.router, tags=["Health"])


app = create_application()
