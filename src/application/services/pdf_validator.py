from src.application.dtos.pdf_dtos import ArchivoEntradaDTO
from src.domain.exceptions.domain_exception import ValidationException
from src.infrastructure.config.settings import get_settings


def restriction_verifier(archivo_dto: ArchivoEntradaDTO):

    settings = get_settings()

    if archivo_dto.extension.lower() != "pdf":
        raise ValidationException("El archivo debe ser un pdf ")

    if len(archivo_dto.contenido) >= settings.PDF_MAX_SIZE_BYTES:
        raise ValidationException("El archivo es demasiado grande")

    if len(archivo_dto.contenido) < settings.PDF_MIN_SIZE_BYTES:
        raise ValidationException("El archivo esta vacio")
