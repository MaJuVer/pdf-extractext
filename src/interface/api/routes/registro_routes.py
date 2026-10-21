"""
Rutas CRUD para RegistroProcesamiento.

Provee los endpoints para:
- GET    /registros             - Listar todos los registros (paginado)
- GET    /registros/{id}        - Obtener un registro por ID
- PUT    /registros/{id}        - Actualizar un registro
- DELETE /registros/{id}        - Eliminar un registro
- GET    /registros/hash/{hash} - Obtener un registro por hash SHA256
"""

import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from src.application.services.actualizar_registro_service import (
    ActualizarRegistroService,
)
from src.application.services.eliminar_registro_service import EliminarRegistroService
from src.application.services.listar_registros_service import ListarRegistrosService
from src.application.services.obtener_por_hash_service import ObtenerPorHashService
from src.application.services.obtener_registro_service import ObtenerRegistroService
from src.interface.api.dependencies.registro_dependencies import (
    get_actualizar_registro_service,
    get_eliminar_registro_service,
    get_listar_registros_service,
    get_obtener_por_hash_service,
    get_obtener_registro_service,
)
from src.interface.api.presenters.registro_presenter import to_response
from src.interface.api.schemas.base_schema import ErrorResponse
from src.interface.api.schemas.registro_schema import (
    RegistroDeleteResponse,
    RegistroListResponse,
    RegistroProcesamientoResponse,
    RegistroProcesamientoUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/registros", tags=["Registros"])

HASH_PATTERN = r"^[a-fA-F0-9]{64}$"


@router.get(
    "",
    response_model=RegistroListResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Parámetros inválidos"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
    summary="Listar registros",
    description="Obtiene una lista paginada de todos los registros de procesamiento.",
)
async def listar_registros(
    service: Annotated[ListarRegistrosService, Depends(get_listar_registros_service)],
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Cantidad de items por página"),
) -> RegistroListResponse:
    """Lista todos los registros con paginación."""
    pagina = service.ejecutar(page=page, page_size=page_size)

    return RegistroListResponse(
        items=[to_response(registro) for registro in pagina.items],
        total=pagina.total,
        page=pagina.page,
        page_size=pagina.page_size,
    )


@router.get(
    "/hash/{hash_contenido}",
    response_model=RegistroProcesamientoResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Registro no encontrado"},
        422: {"model": ErrorResponse, "description": "Hash inválido"},
    },
    summary="Obtener registro por hash",
    description="Busca un registro de procesamiento por su hash SHA256 de contenido.",
)
async def obtener_por_hash(
    hash_contenido: Annotated[str, Path(pattern=HASH_PATTERN)],
    service: Annotated[ObtenerPorHashService, Depends(get_obtener_por_hash_service)],
) -> RegistroProcesamientoResponse:
    """Obtiene un registro por su hash SHA256."""
    registro = service.ejecutar(hash_contenido)

    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún registro con hash: {hash_contenido[:16]}...",
        )

    return to_response(registro)


@router.get(
    "/{id_registro}",
    response_model=RegistroProcesamientoResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Registro no encontrado"},
        422: {"model": ErrorResponse, "description": "ID inválido"},
    },
    summary="Obtener registro por ID",
    description="Obtiene los detalles de un registro específico por su identificador único.",
)
async def obtener_registro(
    id_registro: UUID,
    service: Annotated[ObtenerRegistroService, Depends(get_obtener_registro_service)],
) -> RegistroProcesamientoResponse:
    """Obtiene un registro por su ID."""
    registro = service.ejecutar(str(id_registro))

    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el registro con ID: {id_registro}",
        )

    return to_response(registro)


@router.put(
    "/{id_registro}",
    response_model=RegistroProcesamientoResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Registro no encontrado"},
        422: {"model": ErrorResponse, "description": "Datos inválidos"},
    },
    summary="Actualizar registro",
    description="Actualiza el nombre y/o el contenido extraído de un registro existente.",
)
async def actualizar_registro(
    id_registro: UUID,
    datos_actualizacion: RegistroProcesamientoUpdate,
    service: Annotated[ActualizarRegistroService, Depends(get_actualizar_registro_service)],
) -> RegistroProcesamientoResponse:
    """Actualiza un registro existente."""
    registro = service.ejecutar(
        id_registro=str(id_registro),
        nuevo_texto=datos_actualizacion.contenido_extraido,
        nuevo_nombre_archivo=datos_actualizacion.nombre_archivo_original,
    )

    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el registro con ID: {id_registro}",
        )

    return to_response(registro)


@router.delete(
    "/{id_registro}",
    response_model=RegistroDeleteResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Registro no encontrado"},
        422: {"model": ErrorResponse, "description": "ID inválido"},
    },
    summary="Eliminar registro",
    description="Elimina un registro de procesamiento de la base de datos.",
)
async def eliminar_registro(
    id_registro: UUID,
    service: Annotated[EliminarRegistroService, Depends(get_eliminar_registro_service)],
) -> RegistroDeleteResponse:
    """Elimina un registro por su ID."""
    id_validado = str(id_registro)

    logger.info("Solicitud de eliminación para registro: %s", id_validado)

    eliminado = service.ejecutar(id_validado)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el registro con ID: {id_registro}",
        )

    logger.info("Registro eliminado exitosamente: %s", id_validado)

    return RegistroDeleteResponse(
        eliminado=True,
        id_registro=id_validado,
        mensaje="Registro eliminado exitosamente",
    )
