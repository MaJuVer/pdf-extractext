"""
Servicio para persistir registros de procesamiento.

La detección de duplicados vive en el orquestador (ruta cacheada/nueva).
La unicidad del hash se garantiza en la base de datos mediante el índice
único, por lo que este servicio solo construye y persiste la entidad.
"""

from src.application.dtos.pdf_dtos import (
    RegistroProcesamientoOutputDTO,
    TextoExtraidoDTO,
)
from src.application.mappers.registro_procesamiento_mapper import (
    RegistroProcesamientoMapper,
)
from src.domain.entities.documento_pdf import DocumentoPDF
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class GuardarRegistroService:
    """Servicio para guardar registros de procesamiento PDF."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository
        self._mapper = RegistroProcesamientoMapper()

    def ejecutar(
        self,
        pdf: DocumentoPDF,
        texto_dto: TextoExtraidoDTO,
        hash_contenido: str,
    ) -> RegistroProcesamientoOutputDTO:
        """
        Persiste un nuevo registro de procesamiento.

        Args:
            pdf: Documento PDF procesado.
            texto_dto: DTO con el texto extraído del PDF.
            hash_contenido: Hash SHA256 ya calculado por el orquestador.

        Returns:
            RegistroProcesamientoOutputDTO con el registro guardado.

        Raises:
            DocumentoDuplicadoException: Si el índice único detecta una
                carrera con otro procesamiento del mismo contenido.
        """
        entidad = RegistroProcesamiento(
            nombre_archivo_original=pdf.nombre_archivo,
            contenido_extraido=texto_dto.contenido,
            hash_contenido=hash_contenido,
        )

        entidad_guardada = self._repository.add(entidad)

        return self._mapper.to_dto(entidad_guardada)
