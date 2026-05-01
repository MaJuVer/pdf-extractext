from src.application.dtos.pdf_dtos import (
    RegistroProcesamientoOutputDTO,
    TextoExtraidoDTO,
)
from src.application.mappers.registro_procesamiento_mapper import (
    RegistroProcesamientoMapper,
)
from src.application.services.base_service import BaseService
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.base_repository import BaseRepository


class GuardarRegistroService(BaseService[None, BaseRepository]):
    def __init__(self, repository: BaseRepository[RegistroProcesamiento]) -> None:
        super().__init__(repository)
        self._mapper = RegistroProcesamientoMapper()

    def ejecutar(
        self, pdf: DocumentoPDF, texto_dto: TextoExtraidoDTO
    ) -> RegistroProcesamientoOutputDTO:
        entidad = RegistroProcesamiento(
            nombre_archivo_original=pdf.nombre_archivo,
            contenido_extraido=texto_dto.contenido,
        )

        entidad_guardada = self.repository.add(entidad)

        return self._mapper.to_dto(entidad_guardada)
