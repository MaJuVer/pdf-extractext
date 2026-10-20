from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)


class EliminarRegistroService:
    """Elimina un registro de procesamiento por su ID."""

    def __init__(self, repository: RegistroProcesamientoRepository) -> None:
        self._repository = repository

    def ejecutar(self, id_registro: str) -> bool:
        return self._repository.delete(id_registro)
