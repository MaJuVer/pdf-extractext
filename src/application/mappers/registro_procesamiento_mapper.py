from src.application.dtos.pdf_dtos import RegistroProcesamientoOutputDTO
from src.domain.entities.registro_procesamiento import RegistroProcesamiento


class RegistroProcesamientoMapper:
    """Convierte entidades RegistroProcesamiento a DTOs de salida."""

    def to_dto(self, entity: RegistroProcesamiento) -> RegistroProcesamientoOutputDTO:
        return RegistroProcesamientoOutputDTO(
            id_registro=str(entity.id),
            nombre_archivo_original=entity.nombre_archivo_original,
            longitud_texto=len(entity.contenido_extraido),
            mensaje_confirmacion="Archivo procesado exitosamente",
        )
