"""Tests del ciclo de vida del cliente MongoDB."""

from typing import Iterator

import pytest

from src.infrastructure.config.settings import get_settings
from src.infrastructure.persistence import database


class _ClienteFalso:
    """Cliente mínimo que registra las bases pedidas y si fue cerrado."""

    def __init__(self) -> None:
        self.cerrado = False
        self.bases: list[str] = []

    def get_database(self, nombre: str) -> str:
        self.bases.append(nombre)
        return f"db:{nombre}"

    def close(self) -> None:
        self.cerrado = True


@pytest.fixture(autouse=True)
def _limpiar_caches() -> Iterator[None]:
    database.get_client.cache_clear()
    get_settings.cache_clear()
    yield
    database.get_client.cache_clear()
    get_settings.cache_clear()


def test_get_client_devuelve_siempre_el_mismo_objeto(monkeypatch: pytest.MonkeyPatch) -> None:
    creados: list[_ClienteFalso] = []

    def _crear(_url: str) -> _ClienteFalso:
        cliente = _ClienteFalso()
        creados.append(cliente)
        return cliente

    monkeypatch.setattr(database, "MongoClient", _crear)

    primero = database.get_client()
    segundo = database.get_client()

    assert primero is segundo
    assert len(creados) == 1


def test_get_db_usa_la_base_configurada(monkeypatch: pytest.MonkeyPatch) -> None:
    cliente = _ClienteFalso()
    monkeypatch.setattr(database, "MongoClient", lambda _url: cliente)

    assert next(database.get_db()) == f"db:{get_settings().MONGO_DB}"
    assert cliente.bases == [get_settings().MONGO_DB]


def test_close_client_cierra_y_limpia_el_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    cliente = _ClienteFalso()
    monkeypatch.setattr(database, "MongoClient", lambda _url: cliente)
    database.get_client()

    database.close_client()

    assert cliente.cerrado is True
    assert database.get_client.cache_info().currsize == 0


def test_close_client_sin_cliente_creado_no_falla(monkeypatch: pytest.MonkeyPatch) -> None:
    def _no_debe_crearse(_url: str) -> _ClienteFalso:
        raise AssertionError("no se debe crear un cliente")

    monkeypatch.setattr(database, "MongoClient", _no_debe_crearse)

    database.close_client()
