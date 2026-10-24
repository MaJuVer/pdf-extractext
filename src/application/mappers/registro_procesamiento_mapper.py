from src.application.dtos.pdf_dtos import RegistroProcesamientoOutputDTO
from src.application.dtos.registro_dtos import RegistroDetalleDTO
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

    def to_detalle_dto(self, entity: RegistroProcesamiento) -> RegistroDetalleDTO:
        """Convierte la entidad en un DTO apto para la capa de interface."""
        return RegistroDetalleDTO(
            id=entity.id,
            nombre_archivo_original=entity.nombre_archivo_original,
            contenido_extraido=entity.contenido_extraido,
            hash_contenido=entity.hash_contenido,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
