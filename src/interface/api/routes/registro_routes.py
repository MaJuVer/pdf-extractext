"""
Rutas CRUD para RegistroProcesamiento.

Provee los endpoints para:
- GET    /registros          - Listar todos los registros (paginado)
- GET    /registros/{id}     - Obtener un registro por ID
- PUT    /registros/{id}     - Actualizar un registro
- DELETE /registros/{id}     - Eliminar un registro
- GET    /registros/hash/{hash} - Obtener un registro por hash SHA256
"""

import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.application.services.actualizar_registro_service import ActualizarRegistroService
from src.application.services.eliminar_registro_service import EliminarRegistroService
from src.application.services.obtener_registro_service import ObtenerRegistroService
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.base_repository import BaseRepository
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)
from src.interface.api.dependencies.registro_dependencies import (
    get_actualizar_registro_service,
    get_base_repository,
    get_eliminar_registro_service,
    get_obtener_registro_service,
    get_registro_repository,
)
from src.interface.api.schemas.registro_schema import (
    ErrorResponseSchema,
    RegistroDeleteResponse,
    RegistroListResponse,
    RegistroProcesamientoResponse,
    RegistroProcesamientoUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/registros", tags=["Registros"])


def _validate_uuid(id_registro: str) -> str:
    """Valida que el ID sea un UUID válido."""
    try:
        UUID(id_registro)
        return id_registro
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID de registro inválido: {id_registro}. Debe ser un UUID válido.",
        ) from e


@router.get(
    "",
    response_model=RegistroListResponse,
    responses={
        400: {"model": ErrorResponseSchema, "description": "Parámetros inválidos"},
        500: {"model": ErrorResponseSchema, "description": "Error interno del servidor"},
    },
    summary="Listar registros",
    description="Obtiene una lista paginada de todos los registros de procesamiento.",
)
async def listar_registros(
    repository: Annotated[BaseRepository, Depends(get_base_repository)],
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Cantidad de items por página"),
) -> RegistroListResponse:
    """Lista todos los registros con paginación."""
    skip = (page - 1) * page_size
    all_registros = repository.get_all()
    total = len(all_registros)
    items = all_registros[skip : skip + page_size]
    return RegistroListResponse(
        items=[_entity_to_response(reg) for reg in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/hash/{hash_contenido}",
    response_model=RegistroProcesamientoResponse,
    responses={
        404: {"model": ErrorResponseSchema, "description": "Registro no encontrado"},
        400: {"model": ErrorResponseSchema, "description": "Hash inválido"},
    },
    summary="Obtener registro por hash",
    description="Busca un registro de procesamiento por su hash SHA256 de contenido.",
)
async def obtener_por_hash(
    hash_contenido: str,
    repository: Annotated[RegistroProcesamientoRepository, Depends(get_registro_repository)],
) -> RegistroProcesamientoResponse:
    """Obtiene un registro por su hash SHA256."""
    if len(hash_contenido) != 64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hash inválido. Debe ser un hash SHA256 de 64 caracteres hexadecimales.",
        )

    registro = repository.get_by_hash(hash_contenido)
    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún registro con hash: {hash_contenido[:16]}...",
        )

    return _entity_to_response(registro)


@router.get(
    "/{id_registro}",
    response_model=RegistroProcesamientoResponse,
    responses={
        404: {"model": ErrorResponseSchema, "description": "Registro no encontrado"},
        400: {"model": ErrorResponseSchema, "description": "ID inválido"},
    },
    summary="Obtener registro por ID",
    description="Obtiene los detalles de un registro específico por su identificador único.",
)
async def obtener_registro(
    id_registro: str,
    service: Annotated[ObtenerRegistroService, Depends(get_obtener_registro_service)],
) -> RegistroProcesamientoResponse:
    """Obtiene un registro por su ID."""
    id_validado = _validate_uuid(id_registro)
    registro = service.ejecutar(id_validado)

    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el registro con ID: {id_registro}",
        )

    return _entity_to_response(registro)


@router.put(
    "/{id_registro}",
    response_model=RegistroProcesamientoResponse,
    responses={
        404: {"model": ErrorResponseSchema, "description": "Registro no encontrado"},
        400: {"model": ErrorResponseSchema, "description": "Datos inválidos"},
    },
    summary="Actualizar registro",
    description="Actualiza el contenido extraído de un registro existente.",
)
async def actualizar_registro(
    id_registro: str,
    datos_actualizacion: RegistroProcesamientoUpdate,
    service: Annotated[ActualizarRegistroService, Depends(get_actualizar_registro_service)],
) -> RegistroProcesamientoResponse:
    """Actualiza un registro existente."""
    id_validado = _validate_uuid(id_registro)

    if not datos_actualizacion.nombre_archivo_original and not datos_actualizacion.contenido_extraido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un campo para actualizar.",
        )

    registro = service.ejecutar(
        id_registro=id_validado,
        nuevo_texto=datos_actualizacion.contenido_extraido,
        nuevo_hash=None,
    )

    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el registro con ID: {id_registro}",
        )

    return _entity_to_response(registro)


@router.delete(
    "/{id_registro}",
    response_model=RegistroDeleteResponse,
    responses={
        404: {"model": ErrorResponseSchema, "description": "Registro no encontrado"},
        400: {"model": ErrorResponseSchema, "description": "ID inválido"},
    },
    summary="Eliminar registro",
    description="Elimina un registro de procesamiento de la base de datos.",
)
async def eliminar_registro(
    id_registro: str,
    service: Annotated[EliminarRegistroService, Depends(get_eliminar_registro_service)],
) -> RegistroDeleteResponse:
    """Elimina un registro por su ID."""
    id_validado = _validate_uuid(id_registro)

    logger.info(f"Solicitud de eliminación para registro: {id_validado}")

    eliminado = service.ejecutar(id_validado)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el registro con ID: {id_registro}",
        )

    logger.info(f"Registro eliminado exitosamente: {id_validado}")

    return RegistroDeleteResponse(
        eliminado=True,
        id_registro=id_validado,
        mensaje="Registro eliminado exitosamente",
    )


def _entity_to_response(registro: RegistroProcesamiento) -> RegistroProcesamientoResponse:
    """Convierte una entidad RegistroProcesamiento a response schema."""
    return RegistroProcesamientoResponse(
        id=registro.id,
        nombre_archivo_original=registro.nombre_archivo_original,
        contenido_extraido=registro.contenido_extraido,
        hash_contenido=registro.hash_contenido,
        created_at=registro.created_at,
        updated_at=registro.updated_at,
    )