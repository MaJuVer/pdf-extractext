from functools import lru_cache
from typing import List

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuraciones globales de la aplicación.
    Los valores por defecto evitan errores en MyPy, pero Pydantic
    priorizará los valores que encuentre en tu archivo .env.
    """

    app_name: str = "pdf-extractext"
    app_description: str = "API RESTful para extraer texto de archivos PDF"
    app_version: str = "0.1.0"
    debug: bool = True
    cors_origins: List[str] = ["*"]

    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PDF_MAX_SIZE_BYTES: int
    PDF_MIN_SIZE_BYTES: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}?authSource=admin"


@lru_cache
def get_settings() -> Settings:
    """Instancia y devuelve las configuraciones."""
    return Settings()
