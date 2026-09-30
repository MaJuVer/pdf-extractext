from src.domain.repositories.base_repository import BaseRepository


class EliminarRegistroService:
    def __init__(self, repository: BaseRepository):
        # Inyectamos el repositorio al igual que en los otros servicios
        self.repository = repository

    def ejecutar(self, id_registro: str) -> bool:
        return self.repository.delete(id_registro)
