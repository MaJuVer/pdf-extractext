from src.domain.repositories.base_repository import BaseRepository

class EliminarRegistroService:
    def __init__(self, repository: BaseRepository):
        # Inyectamos el repositorio al igual que en los otros servicios
        self.repository = repository

    def ejecutar(self, id_registro) -> bool:
        # Delegamos la responsabilidad de eliminar al repositorio 
        # y devolvemos el resultado (True si se borró, False si no existía)
        return self.repository.eliminar_por_id(id_registro)
