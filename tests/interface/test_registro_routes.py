"""Tests de integración HTTP para el CRUD /registros."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.application.services.actualizar_registro_service import (
    ActualizarRegistroService,
)
from src.application.services.eliminar_registro_service import EliminarRegistroService
from src.application.services.listar_registros_service import ListarRegistrosService
from src.application.services.obtener_por_hash_service import ObtenerPorHashService
from src.application.services.obtener_registro_service import ObtenerRegistroService
from src.domain.entities.registro_procesamiento import RegistroProcesamiento
from src.domain.repositories.registro_procesamiento_repository import (
    RegistroProcesamientoRepository,
)
from src.interface.api.dependencies.registro_dependencies import (
    get_actualizar_registro_service,
    get_eliminar_registro_service,
    get_listar_registros_service,
    get_obtener_por_hash_service,
    get_obtener_registro_service,
)
from src.interface.main import app

client = TestClient(app)

HASH_A = "a" * 64
HASH_B = "b" * 64


class FakeRegistroRepository(RegistroProcesamientoRepository):
    """Repositorio en memoria para tests HTTP."""

    def __init__(self, registros: list[RegistroProcesamiento]) -> None:
        self._registros = {str(registro.id): registro for registro in registros}

    def get_by_id(self, entity_id: str) -> RegistroProcesamiento | None:
        return self._registros.get(entity_id)

    def get_all(self) -> list[RegistroProcesamiento]:
        return list(self._registros.values())

    def get_paginated(self, skip: int, limit: int) -> tuple[list[RegistroProcesamiento], int]:
        registros = list(self._registros.values())
        return registros[skip : skip + limit], len(registros)

    def add(self, entity: RegistroProcesamiento) -> RegistroProcesamiento:
        self._registros[str(entity.id)] = entity
        return entity

    def update(self, entity: RegistroProcesamiento) -> RegistroProcesamiento:
        self._registros[str(entity.id)] = entity
        return entity

    def delete(self, entity_id: str) -> bool:
        return self._registros.pop(entity_id, None) is not None

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._registros

    def get_by_hash(self, hash_contenido: str) -> RegistroProcesamiento | None:
        for registro in self._registros.values():
            if registro.hash_contenido == hash_contenido:
                return registro
        return None


@pytest.fixture
def repo() -> FakeRegistroRepository:
    return FakeRegistroRepository(
        [
            RegistroProcesamiento(
                nombre_archivo_original="uno.pdf",
                contenido_extraido="Texto uno",
                hash_contenido=HASH_A,
            ),
            RegistroProcesamiento(
                nombre_archivo_original="dos.pdf",
                contenido_extraido="Texto dos",
                hash_contenido=HASH_B,
            ),
        ]
    )


@pytest.fixture(autouse=True)
def _overrides(repo: FakeRegistroRepository) -> None:
    app.dependency_overrides[get_listar_registros_service] = lambda: ListarRegistrosService(repo)
    app.dependency_overrides[get_obtener_registro_service] = lambda: ObtenerRegistroService(repo)
    app.dependency_overrides[get_obtener_por_hash_service] = lambda: ObtenerPorHashService(repo)
    app.dependency_overrides[get_actualizar_registro_service] = lambda: ActualizarRegistroService(repo)
    app.dependency_overrides[get_eliminar_registro_service] = lambda: EliminarRegistroService(repo)
    yield
    app.dependency_overrides.clear()


def _primer_registro(repo: FakeRegistroRepository) -> RegistroProcesamiento:
    return repo.get_all()[0]


def test_listar_registros_paginado(repo: FakeRegistroRepository) -> None:
    response = client.get("/registros?page=1&page_size=1")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert len(data["items"]) == 1


def test_obtener_registro_por_id(repo: FakeRegistroRepository) -> None:
    registro = _primer_registro(repo)

    response = client.get(f"/registros/{registro.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(registro.id)


def test_obtener_registro_inexistente_404() -> None:
    assert client.get(f"/registros/{uuid4()}").status_code == 404


def test_obtener_registro_id_invalido_422() -> None:
    assert client.get("/registros/no-es-uuid").status_code == 422


def test_obtener_por_hash(repo: FakeRegistroRepository) -> None:
    response = client.get(f"/registros/hash/{HASH_A}")

    assert response.status_code == 200
    assert response.json()["hash_contenido"] == HASH_A


def test_obtener_por_hash_inexistente_404() -> None:
    assert client.get(f"/registros/hash/{'c' * 64}").status_code == 404


def test_obtener_por_hash_invalido_422() -> None:
    assert client.get("/registros/hash/abc").status_code == 422


def test_actualizar_texto_y_nombre(repo: FakeRegistroRepository) -> None:
    registro = _primer_registro(repo)

    response = client.put(
        f"/registros/{registro.id}",
        json={
            "contenido_extraido": "Texto actualizado",
            "nombre_archivo_original": "renombrado.pdf",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["contenido_extraido"] == "Texto actualizado"
    assert data["nombre_archivo_original"] == "renombrado.pdf"


def test_actualizar_sin_campos_422(repo: FakeRegistroRepository) -> None:
    registro = _primer_registro(repo)

    assert client.put(f"/registros/{registro.id}", json={}).status_code == 422


def test_actualizar_inexistente_404() -> None:
    response = client.put(
        f"/registros/{uuid4()}",
        json={"contenido_extraido": "x"},
    )

    assert response.status_code == 404


def test_eliminar_registro(repo: FakeRegistroRepository) -> None:
    registro = _primer_registro(repo)

    response = client.delete(f"/registros/{registro.id}")

    assert response.status_code == 200
    assert response.json()["eliminado"] is True
    assert client.get(f"/registros/{registro.id}").status_code == 404


def test_eliminar_inexistente_404() -> None:
    assert client.delete(f"/registros/{uuid4()}").status_code == 404
