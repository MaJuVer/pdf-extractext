from src.domain.repositories.base_repository import BaseRepository

class ObtenerRegistroService:
    def __init__(self, repository: BaseRepository):
        # Inyectamos el repositorio (en el test será el Mock, en prod será el de Mongo)
        self.repository = repository

    def ejecutar(self, id_registro):
        # Le pedimos al repositorio que busque el registro por ID
        registro = self.repository.obtener_por_id(id_registro)
        
        
        return registro
