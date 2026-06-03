from src.application.dtos.base_dto import EmptyInputDTO
from src.application.dtos.pdf_dtos import RegistroProcesamientoOutputDTO
from src.application.mappers.base_mapper import BaseMapper
from src.domain.entities.registro_procesamiento import RegistroProcesamiento


class RegistroProcesamientoMapper(
    BaseMapper[RegistroProcesamiento, EmptyInputDTO, RegistroProcesamientoOutputDTO]
):
    def to_entity(self, dto: EmptyInputDTO) -> RegistroProcesamiento:
        raise NotImplementedError("No se usa en este caso")

    def to_dto(self, entity: RegistroProcesamiento) -> RegistroProcesamientoOutputDTO:
        return RegistroProcesamientoOutputDTO(
            id_registro=str(entity.id),
            nombre_archivo_original=entity.nombre_archivo_original,
            longitud_texto=len(entity.contenido_extraido),
            mensaje_confirmacion="Archivo procesado exitosamente",
        )
