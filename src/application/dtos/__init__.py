"""Data Transfer Objects para la capa de aplicación."""

from src.application.dtos.pdf_dtos import (
    ArchivoEntradaDTO,
    ArchivoSalidaDTO,
    RegistroProcesamientoOutputDTO,
    TextoExtraidoDTO,
)
from src.application.dtos.registro_dtos import RegistrosPaginadosDTO

__all__ = [
    "ArchivoEntradaDTO",
    "ArchivoSalidaDTO",
    "TextoExtraidoDTO",
    "RegistroProcesamientoOutputDTO",
    "RegistrosPaginadosDTO",
]
