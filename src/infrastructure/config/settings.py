from typing import List
from functools import lru_cache
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configuraciones globales de la aplicación.
    """
    # Atributos globales de la aplicación
    app_name: str = "pdf-extractext"
    app_description: str = "API RESTful para extraer texto de archivos PDF"
    app_version: str = "0.1.0"
    
    # Seguridad (Configuración segura para producción)
    debug: bool = True
    cors_origins: List[str] = ["*"]

    # Componentes de la base de datos (Sin hardcodear en la URL)
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_HOST: str = "mongodb" 
    MONGO_PORT: int = 27017
    MONGO_DB: str = "pdf-extractext"

    # Restricciones de archivos
    max_size: int 
    min_size: int 

    # Configuración de Pydantic para leer el .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # El Factor IV de 12-Factor App: Construcción correcta desde componentes
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}?authSource=admin"

@lru_cache
def get_settings() -> Settings:
    return Settings()