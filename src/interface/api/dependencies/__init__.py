"""
Dependencias inyectables.

Define dependencias que pueden ser inyectadas en endpoints
usando FastAPI dependency injection system.

Ejemplo:
    - get_db_session
    - get_current_user
    - get_pdf_orchestrator
"""

from src.interface.api.dependencies.pdf_dependencies import get_pdf_orchestrator

__all__ = ["get_pdf_orchestrator"]