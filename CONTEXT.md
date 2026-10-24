# Contexto de testing

Este documento fija los *seams* de la suite: qué se prueba en cada capa, con qué
doble y dónde vive el test. La intención es que cualquier cambio nuevo se ubique
en el mismo lugar y use el mismo tipo de doble.

## Seams

| Seam | Dónde | Doble |
|---|---|---|
| Entidades de dominio | `tests/domain/` | ninguno (lógica pura) |
| Casos de uso | `tests/application/test_services/` | `MagicMock(spec=RegistroProcesamientoRepository)` / fakes que implementan la interfaz |
| Orquestador | `tests/application/test_services/test_procesar_pdf_orchestrator.py` | `MagicMock(spec=...)` del repositorio y del extractor |
| Repositorio Mongo | `tests/infrastructure/` | `mongomock` |
| Base de datos e índices | `tests/infrastructure/` | `mongomock` + `monkeypatch` de `MongoClient` |
| HTTP | `tests/interface/` | `TestClient` + `app.dependency_overrides` |
| Arquitectura | `tests/test_arquitectura.py` | AST de la stdlib (sin ejecutar la app) |

## Reglas

1. Todo `MagicMock` de una interfaz propia lleva `spec=` con la interfaz o la
   entidad que reemplaza. Así un cambio de contrato rompe el test en vez de
   pasar silenciosamente.
2. Los tests afirman comportamiento observable (resultado, excepción, efecto
   persistido). Solo se verifica la forma de invocar a un colaborador cuando el
   caso de uso es delegación pura.
3. Los fakes que implementan una interfaz propia se declaran heredando de ella,
   no con `MagicMock` sin `spec`.
4. El test de arquitectura en `tests/test_arquitectura.py` es la guardia de las
   dependencias entre capas: `domain` ← `application` ← `infrastructure` /
   `interface`. Los imports solo cruzan en `interface/api/dependencies/`.
