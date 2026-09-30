from typing import Optional

from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.base_repository import BaseRepository


class ActualizarRegistroService:
    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    def ejecutar(
        self,
        id_registro: str,
        nuevo_texto: str | None = None,
        nuevo_hash: str | None = None,
    ) -> Optional[RegistroProcesamiento]:
        registro = self.repository.get_by_id(id_registro)

        if registro:
            if nuevo_texto is not None:
                registro.contenido_extraido = nuevo_texto
            if nuevo_hash is not None:
                registro.hash_contenido = nuevo_hash
            return self.repository.update(registro)

        return None