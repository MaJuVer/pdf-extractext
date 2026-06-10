from typing import Optional

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.base_repository import BaseRepository


class ObtenerRegistroService:
    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    def ejecutar(self, id_registro: str) -> Optional[RegistroProcesamiento]:
        return self.repository.get_by_id(id_registro)