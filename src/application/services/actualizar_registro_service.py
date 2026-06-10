from src.domain.repositories.base_repository import BaseRepository

class ActualizarRegistroService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def ejecutar(self, id_registro, nuevo_texto: str, nuevo_hash: str):
        # 1. Buscamos el registro original en la base de datos
        registro = self.repository.obtener_por_id(id_registro)
        
        if registro:
            # 2. Pisamos los datos viejos con los nuevos
            registro.contenido_extraido = nuevo_texto
            registro.hash_contenido = nuevo_hash
            
            # 3. Le decimos al repositorio que persista los cambios
            self.repository.actualizar(registro)
            
        # 4. Devolvemos el registro con la información actualizada
        return registro
