"""Guardia automática de las dependencias permitidas entre capas."""

import ast
from pathlib import Path

PROHIBIDOS = {
    "domain": {"application", "infrastructure", "interface"},
    "application": {"infrastructure", "interface"},
    "infrastructure": {"interface"},
}


def violaciones(raiz: Path) -> list[tuple[str, int, str]]:
    """Devuelve (archivo, linea, modulo) por cada import de capa prohibido."""
    resultado: list[tuple[str, int, str]] = []
    for capa, prohibidas in PROHIBIDOS.items():
        for archivo in (raiz / "src" / capa).rglob("*.py"):
            arbol = ast.parse(archivo.read_text(encoding="utf-8"))
            for nodo in ast.walk(arbol):
                if isinstance(nodo, ast.ImportFrom) and nodo.module:
                    modulos = [nodo.module]
                elif isinstance(nodo, ast.Import):
                    modulos = [alias.name for alias in nodo.names]
                else:
                    continue
                for modulo in modulos:
                    partes = modulo.split(".")
                    if len(partes) > 1 and partes[0] == "src" and partes[1] in prohibidas:
                        resultado.append((str(archivo), nodo.lineno, modulo))
    return resultado


def test_violaciones_detecta_import_prohibido(tmp_path: Path) -> None:
    archivo = tmp_path / "src" / "application" / "x.py"
    archivo.parent.mkdir(parents=True)
    archivo.write_text(
        "from src.infrastructure.config.settings import get_settings\n",
        encoding="utf-8",
    )

    assert violaciones(tmp_path) == [(str(archivo), 1, "src.infrastructure.config.settings")]


def test_violaciones_detecta_import_absoluto_prohibido(tmp_path: Path) -> None:
    archivo = tmp_path / "src" / "domain" / "x.py"
    archivo.parent.mkdir(parents=True)
    archivo.write_text("import src.interface.main\n", encoding="utf-8")

    assert violaciones(tmp_path) == [(str(archivo), 1, "src.interface.main")]


def test_violaciones_ignora_imports_permitidos(tmp_path: Path) -> None:
    archivo = tmp_path / "src" / "application" / "x.py"
    archivo.parent.mkdir(parents=True)
    archivo.write_text(
        "from src.domain.entities.registro_procesamiento import RegistroProcesamiento\n",
        encoding="utf-8",
    )

    assert violaciones(tmp_path) == []


def test_el_repositorio_cumple_las_reglas_de_dependencias() -> None:
    raiz = Path(__file__).resolve().parents[1]

    assert violaciones(raiz) == []
