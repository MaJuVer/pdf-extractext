"""
Servicio para guardar registros de procesamiento con verificación de duplicados.

Este servicio encapsula la lógica de negocio para:
1. Calcular el hash SHA256 del PDF
2. Verificar si ya existe un registro con ese hash
3. Si existe: lanzar DocumentoDuplicadoException
4. Si no existe: guardar normalmente
"""

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
from src.domain.exceptions.domain_exception import DocumentoDuplicadoException
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class GuardarRegistroService(BaseService[None, RegistroProcesamientoRepository]):
    """
    Servicio para guardar registros de procesamiento PDF.

    Verifica duplicados por hash SHA256 antes de persistir.
    """

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        super().__init__(repository)
        self._mapper = RegistroProcesamientoMapper()

    def ejecutar(
        self, pdf: DocumentoPDF, texto_dto: TextoExtraidoDTO
    ) -> RegistroProcesamientoOutputDTO:
        """
        Guarda un nuevo registro de procesamiento si no existe duplicado.

        Args:
            pdf: Documento PDF procesado.
            texto_dto: DTO con el texto extraído del PDF.

        Returns:
            RegistroProcesamientoOutputDTO con el registro guardado.

        Raises:
            DocumentoDuplicadoException: Si el hash SHA256 ya existe en BD.
        """
        hash_contenido = pdf.calcular_hash_sha256()

        if self.repository.find_by_hash(hash_contenido) is not None:
            raise DocumentoDuplicadoException(
                hash_contenido=hash_contenido,
            )

        entidad = RegistroProcesamiento(
            nombre_archivo_original=pdf.nombre_archivo,
            contenido_extraido=texto_dto.contenido,
            hash_contenido=hash_contenido,
        )

        entidad_guardada = self.repository.add(entidad)

        return self._mapper.to_dto(entidad_guardada)
