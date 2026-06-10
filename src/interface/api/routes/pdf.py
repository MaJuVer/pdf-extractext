"""
Rutas para el procesamiento de archivos PDF.

Provee el endpoint POST /pdf/process para convertir PDFs a TXT.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from src.application.dtos.pdf_dtos import ArchivoEntradaDTO
from src.application.services.procesar_pdf_orchestrator import ProcesarPdfOrchestrator
from src.domain.exceptions.domain_exception import DocumentoDuplicadoException, ValidationException
from src.domain.exceptions.pdf_exceptions import (
    DocumentoSinTextoException,
    PDFExtractionException,
    PDFInvalidException,
)
from src.interface.api.dependencies.pdf_dependencies import get_pdf_orchestrator
from src.interface.api.schemas.base_schema import ErrorResponse

router = APIRouter(prefix="/pdf", tags=["PDF"])


def _validate_filename(filename: str | None) -> str:
    """
    Extrae solo el nombre base del archivo, eliminando path traversal.

    Args:
        filename: Nombre original del archivo.

    Returns:
        Nombre sanitizado del archivo.
    """
    if not filename:
        return "documento.pdf"
    return filename.split("/")[-1].split("\\")[-1]


@router.post(
    "/process",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {"text/plain": {}},
            "description": "Archivo TXT generado",
        },
        400: {
            "model": ErrorResponse,
            "description": "Error de validacion",
        },
        422: {
            "model": ErrorResponse,
            "description": "PDF invalido o sin texto",
        },
    },
    summary="Procesar PDF",
    description="Recibe un archivo PDF y devuelve su contenido como archivo TXT.",
)
async def procesar_pdf(
    file: UploadFile = File(...),
    orchestrator: ProcesarPdfOrchestrator = Depends(get_pdf_orchestrator),
) -> StreamingResponse:
    """
    Procesa un archivo PDF y devuelve el texto extraido como TXT.

    Args:
        file: Archivo PDF subido por el usuario.
        orchestrator: Orquestador con la logica de negocio.

    Returns:
        StreamingResponse con el archivo .txt para descarga.

    Raises:
        HTTPException: Si el archivo no es PDF valido o falla el procesamiento.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no soportado: {file.content_type}. Solo se acepta PDF.",
        )

    contenido = await file.read()
    nombre_sanitizado = _validate_filename(file.filename)

    archivo_dto = ArchivoEntradaDTO(
        nombre=nombre_sanitizado,
        contenido=contenido,
        extension="pdf",
    )

    try:
        resultado = orchestrator.execute(archivo_dto)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except PDFInvalidException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e
    except DocumentoSinTextoException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e
    except DocumentoDuplicadoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except PDFExtractionException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar el PDF",
        ) from e

    resultado.archivo_salida.buffer.seek(0)

    return StreamingResponse(
        content=resultado.archivo_salida.buffer,
        media_type=resultado.archivo_salida.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{resultado.archivo_salida.nombre}"',
        },
    )