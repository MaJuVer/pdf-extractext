"""
Factory de dependencias para el procesamiento de PDF.

Crea las instancias de las dependencias del orquestador
(extractor, repository) siguiendo el patron Factory.
"""

from src.application.services.procesar_pdf_orchestrator import ProcesarPdfOrchestrator
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.infrastructure.external_services.pypdf_extractor import PyPDFExtractor
from src.infrastructure.persistence.database import get_db
from src.infrastructure.persistence.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoMongoRepositoryImpl,
)


def get_pdf_orchestrator() -> ProcesarPdfOrchestrator:
    """
    Factory que crea una instancia del orquestador con sus dependencias.

    Returns:
        ProcesarPdfOrchestrator: Instancia configurada del orquestador.
    """
    db = next(get_db())
    repository = RegistroProcesamientoMongoRepositoryImpl(
        db=db,
        collection_name="registros",
        entity_class=RegistroProcesamiento,
    )
    extractor = PyPDFExtractor()
    return ProcesarPdfOrchestrator(extractor=extractor, repository=repository)