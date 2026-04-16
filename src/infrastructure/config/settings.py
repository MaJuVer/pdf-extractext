from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuraciones globales de la aplicación.
    Los valores por defecto evitan errores en MyPy, pero Pydantic
    priorizará los valores que encuentre en tu archivo .env.
    """
    
    # Atributos de la aplicación que lee main.py
    app_name: str = "pdf-extractext"
    app_description: str = "API RESTful para extraer texto de archivos PDF"
    app_version: str = "0.1.0"
    debug: bool = True
    cors_origins: List[str] = ["*"]
    
    # Atributos de Base de Datos
    database_url: str = "mongodb://localhost:27017"
    database_name: str = "mi_saas_db"

    # Configuración de Pydantic para leer el .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings() -> Settings:
    """Instancia y devuelve las configuraciones."""
    return Settings()