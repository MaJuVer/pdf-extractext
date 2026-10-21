"""Configuración común de la suite.

Fija valores mínimos de entorno antes de importar la aplicación para que
`uv run pytest` funcione en un clon limpio, sin un `.env` local.
"""

import os

os.environ.setdefault("MONGO_USER", "test")
os.environ.setdefault("MONGO_PASS", "test")
os.environ.setdefault("MONGO_HOST", "localhost")
os.environ.setdefault("MONGO_PORT", "27017")
os.environ.setdefault("MONGO_DB", "pdf-extractext-test")
os.environ.setdefault("max_size", "10485760")
os.environ.setdefault("min_size", "1")
