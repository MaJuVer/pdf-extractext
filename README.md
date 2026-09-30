# PDF-ExtractExt

API RESTful construida con **FastAPI** para extraer texto de archivos PDF. Permite subir un PDF, obtener su contenido como `.txt` descargable y mantener un historial de procesados con detección de duplicados por hash SHA256.

El proyecto está diseñado bajo **Clean Architecture** para mantener un código mantenible, testeable y desacoplado de frameworks.

## Stack Tecnológico

| Tecnología          | Propósito                                                |
|---------------------|-----------------------------------------------------------|
| Python 3.11+        | Lenguaje principal                                       |
| FastAPI             | Framework web ASGI de alto rendimiento                   |
| Uvicorn             | Servidor ASGI para producción                            |
| Pydantic v2         | Validación de datos y configuración tipada               |
| pymongo             | Driver oficial de MongoDB                                |
| MongoDB 8.2         | Persistencia NoSQL                                        |
| pypdf               | Extracción de texto desde PDF                             |
| python-multipart    | Parseo de uploads `multipart/form-data`                   |
| UV                  | Gestor de dependencias y entornos virtuales               |
| pytest + coverage   | Tests unitarios y reporte de cobertura                    |
| mypy (strict)       | Type checking estático                                    |
| Ruff                | Linter y formateador                                       |
| Docker Compose      | Orquestación de app + base de datos                       |

## Arquitectura

El proyecto implementa **Clean Architecture** (Robert C. Martin). Las dependencias siempre apuntan hacia el dominio; ninguna capa interna conoce frameworks, bases de datos ni el framework web.

```
┌─────────────────────────────────────────────┐
│   Infrastructure Layer                       │
│   ┌───────────────────────────────────────┐ │
│   │   Interface Layer (FastAPI)           │ │
│   │   ┌───────────────────────────────┐   │ │
│   │   │   Application Layer           │   │ │
│   │   │   ┌───────────────────┐       │   │ │
│   │   │   │   Domain Layer    │       │   │ │
│   │   │   │   • Entities      │       │   │ │
│   │   │   │   • Value Objects │       │   │ │
│   │   │   │   • Repositories  │       │   │ │
│   │   │   │   • Exceptions    │       │   │ │
│   │   │   └───────────────────┘       │   │ │
│   │   └───────────────────────────────┘   │ │
│   └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

| Capa            | Responsabilidad                                                                |
|------------------|---------------------------------------------------------------------------------|
| Domain           | Entidades, value objects, interfaces de repositorio y excepciones de negocio    |
| Application      | Casos de uso, DTOs, mappers y orquestadores                                     |
| Infrastructure   | Persistencia (MongoDB), servicios externos (`pypdf`), configuración y logging   |
| Interface        | Rutas HTTP, schemas Pydantic, dependencias inyectables y `main.py` de FastAPI   |

Flujo de dependencias:

```
Interface (Controllers) → Application (Services) → Domain (Repository interfaces)
                                                   ← Infrastructure (Repository implementations)
```

## Principios Utilizados

- **SRP** — Single Responsibility: cada clase tiene una única razón para cambiar.
- **DIP** — Dependency Inversion: las capas internas definen interfaces; las externas las implementan.
- **OCP** — Open/Closed: la funcionalidad se extiende sin modificar código existente.
- **LSP** — Liskov Substitution: las implementaciones de repositorio son intercambiables.
- **ISP** — Interface Segregation: interfaces específicas (`PDFExtractorInterface`, `BaseRepository`) en lugar de contratos genéricos.
- **DRY** — Don't Repeat Yourself: lógica de negocio centralizada en la capa de aplicación.
- **KISS** — Keep It Simple: soluciones simples antes que complejas y difícilmente mantenibles.
- **Clean Code (Uncle Bob)** — nombres intención-reveladores, funciones cortas con un solo nivel de abstracción, comentarios solo cuando aportan valor real, manejo de errores por excepciones específicas propias del dominio.
- **12-Factor App** — configuración externalizada vía variables de entorno, separación clara de stages y construcción reproducible con `uv.lock` + `Dockerfile` multi-stage.

## Estructura del Proyecto

```
pdf-extractext/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── repositories/
│   │   ├── exceptions/
│   │   └── events/
│   ├── application/
│   │   ├── services/
│   │   ├── dtos/
│   │   ├── interfaces/
│   │   └── mappers/
│   ├── infrastructure/
│   │   ├── persistence/
│   │   │   └── repositories/
│   │   ├── external_services/
│   │   ├── logging/
│   │   └── config/
│   └── interface/
│       └── api/
│           ├── routes/
│           ├── middleware/
│           ├── dependencies/
│           └── schemas/
│       └── main.py
├── tests/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interface/
│   └── test_setup.py
├── docs/
├── data/
├── htmlcov/
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.app.yml
├── docker-compose.db.yml
├── .env.example
├── .env
├── .python-version
├── .gitignore
├── .dockerignore
├── LICENSE
└── README.md
```

## Requisitos

- Python ≥ 3.11 (gestionado vía UV si se usan los comandos locales; en Docker la imagen ya lo trae).
- [UV](https://docs.astral.sh/uv/getting-started/installation/) — gestor de dependencias y entornos virtuales.
- Docker y Docker Compose — necesarios para correr la API y MongoDB en contenedores.
- MongoDB 7+ accesible (local o en contenedor).

## Puesta en funcionamiento

Levanta la **API** y **MongoDB** en contenedores separados pero conectados por una red compartida. Es la vía recomendada porque reproduce el entorno de producción y mantiene la base de datos aislada y persistente.

### 1. Instalar UV (solo la primera vez)

Es el gestor de dependencias usado por el `Dockerfile`. El binario se invoca dentro del build aunque la app corra en contenedor, por lo que se necesita disponible en la máquina para preparar el lock reproducible.

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clonar el repositorio

```bash
git clone https://github.com/MaJuVer/pdf-extractext.git
cd pdf-extractext
```

### 3. Preparar el archivo de variables de entorno

Copiar el template y completar los valores. El archivo real (`.env`) no debe versionarse.

```bash
cp .env.example .env
```

Variables requeridas (alineadas con `Settings` en `src/infrastructure/config/settings.py`):

| Variable    | Descripción                          | Ejemplo                  |
|-------------|---------------------------------------|---------------------------|
| MONGO_USER  | Usuario root de MongoDB               | admin                     |
| MONGO_PASS  | Password del usuario root             | valor seguro              |
| MONGO_HOST  | Host del servicio MongoDB             | mongodb (red Compose)     |
| MONGO_PORT  | Puerto de MongoDB                     | 27017                     |
| MONGO_DB    | Nombre de la base                     | pdf-extractext            |
| debug       | Modo debug de FastAPI (true/false)    | true       |
| MAX_SIZE    | Tamaño máximo del PDF en bytes        | 20971520 (20 MB)          |
| MIN_SIZE    | Tamaño mínimo del PDF en bytes        | 1                         |

### 4. Crear la red compartida (una sola vez)

Ambos `docker-compose` (`db.yml` y `app.yml`) declaran la red como `external`, por lo que debe existir antes del primer `up`.

```bash
docker network create shared-app-network
```

### 5. Levantar MongoDB

```bash
docker compose -f docker-compose.db.yml --env-file .env up -d
```

Esto inicia el contenedor `mongodb_db` con volumen persistente en `./data/mongo`.

### 6. Levantar la API

```bash
docker compose -f docker-compose.app.yml --env-file .env up -d --build
```

La API quedará escuchando en `http://localhost:8000`.

### 7. Verificar el estado del servicio

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{"status":"healthy","timestamp":"...","version":"0.1.0"}
```

### 8. Probar el flujo principal

Subir un PDF y descargar el `.txt`:

```bash
curl -X POST http://localhost:8000/pdf/process \
  -F "file=@./ejemplo.pdf" \
  -o texto_extraido.txt
```

O puedes ir a (si colocaste debug=true):
```bash
http://localhost:8000/docs
```


Listar los registros persistidos:

```bash
curl http://localhost:8000/registros
```


### 9. Apagar los servicios

```bash
docker compose -f docker-compose.app.yml down
docker compose -f docker-compose.db.yml down
```

Los datos permanecen en `./data/mongo`.

## Endpoints

| Método | Endpoint                  | Descripción                                       |
|--------|----------------------------|----------------------------------------------------|
| GET    | `/health`                  | Health check del servicio                          |
| GET    | `/health/ready`            | Readiness check                                     |
| POST   | `/pdf/process`             | Recibe un PDF y devuelve el texto extraído como `.txt` |
| GET    | `/registros`                | Lista paginada de registros                         |
| GET    | `/registros/{id}`          | Obtiene un registro por UUID                        |
| GET    | `/registros/hash/{hash}`   | Obtiene un registro por hash SHA256                 |
| PUT    | `/registros/{id}`          | Actualiza el contenido extraído de un registro      |
| DELETE | `/registros/{id}`          | Elimina un registro                                 |

## Testing, Lint y Type-check

Ejecutar todos los tests con cobertura:

```bash
uv run pytest
```

Linter y formateador:

```bash
uv run ruff check .
uv run ruff format .
```

Type checking estricto:

```bash
uv run mypy src
```

Reporte HTML de cobertura disponible en `htmlcov/index.html`.

## Licencia

MIT — ver archivo [LICENSE](LICENSE).

Copyright (c) 2026 MaJuVer
