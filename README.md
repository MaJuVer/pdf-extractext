# PDF-ExtractExt

API RESTful construida con **FastAPI** para extraer texto de archivos PDF. Proyecto desarrollado siguiendo los principios de **Clean Architecture** para garantizar código mantenible, testeable y escalable.

## Stack Tecnológico

| Tecnología | Propósito |
|------------|-----------|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web de alto rendimiento para APIs |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI para ejecutar la aplicación |
| [MongoDB](https://www.mongodb.com/) | Base de datos NoSQL para persistencia |
| [UV](https://docs.astral.sh/uv/) | Gestor de paquetes y entornos virtuales ultrarrápido |
| [PyTest](https://docs.pytest.org/) | Framework de testing con cobertura |
| [MyPy](https://mypy.readthedocs.io/) | Type checker estático para Python |
| [Ruff](https://docs.astral.sh/ruff/) | Linter y formateador ultrarrápido |
| [Pydantic](https://docs.pydantic.dev/) | Validación de datos y settings |

## Arquitectura

Este proyecto implementa **Clean Architecture** (Arquitectura Limpia) propuesta por Robert C. Martin (Uncle Bob), organizando el código en capas concéntricas donde las dependencias apuntan siempre hacia adentro.

```
┌─────────────────────────────────────────────┐
│   Infrastructure Layer                       │
│   ┌───────────────────────────────────────┐  │
│   │   Interface Layer (FastAPI)          │  │
│   │   ┌───────────────────────────────┐   │  │
│   │   │   Application Layer         │   │  │
│   │   │   ┌───────────────────┐     │   │  │
│   │   │   │   Domain Layer     │     │   │  │
│   │   │   │   • Entities       │     │   │  │
│   │   │   │   • Value Objects  │     │   │  │
│   │   │   │   • Repositories   │     │   │  │
│   │   │   │   • Exceptions     │     │   │  │
│   │   │   └───────────────────┘     │   │  │
│   │   │                               │   │  │
│   │   └───────────────────────────────┘   │  │
│   └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Principios Aplicados

- **SRP** (Single Responsibility Principle): Cada clase tiene una única razón para cambiar
- **DIP** (Dependency Inversion Principle): Las capas interiores definen interfaces, las exteriores implementan
- **OCP** (Open/Closed Principle): Extiende funcionalidad sin modificar código existente
- **DRY** (Don't Repeat Yourself): Evita la duplicación de lógica de negocio
- **KISS** (Keep It Simple, Stupid): Soluciones simples sobre complejas

## Estructura del Proyecto

```
pdf-extractext/
├── src/
│   ├── domain/                    # Capa de Dominio (núcleo de negocio)
│   │   ├── entities/              # Entidades de negocio
│   │   ├── value_objects/         # Objetos de valor inmutables
│   │   ├── repositories/          # Interfaces de repositorios (DIP)
│   │   ├── exceptions/            # Excepciones de dominio
│   │   └── events/                # Eventos de dominio
│   │
│   ├── application/               # Capa de Aplicación
│   │   ├── services/              # Casos de uso / Servicios
│   │   ├── dtos/                  # Data Transfer Objects
│   │   ├── interfaces/            # Interfaces de servicios externos
│   │   └── mappers/               # Conversores Entity <-> DTO
│   │
│   ├── infrastructure/            # Capa de Infraestructura
│   │   ├── persistence/           # Implementaciones de persistencia
│   │   │   └── repositories/      # Implementaciones concretas de repos
│   │   ├── external_services/     # Clientes de APIs externas
│   │   ├── logging/               # Implementación de logging
│   │   └── config/                # Configuraciones (Settings, env vars)
│   │
│   └── interface/                 # Capa de Interface (Adaptadores)
│       ├── api/                   # Endpoints REST
│       │   ├── routes/            # Agrupación de rutas
│       │   ├── middleware/        # Middleware de FastAPI
│       │   ├── dependencies/      # Dependencias inyectables
│       │   └── schemas/           # Schemas Pydantic para requests/responses
│       └── main.py                # Punto de entrada FastAPI
│
├── tests/                         # Tests siguiendo estructura src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interface/
│
├── docs/                          # Documentación adicional
├── scripts/                       # Scripts utilitarios
├── .env.example                   # Template de variables de entorno
├── .env                           # Variables de entorno (no commitear)
├── .python-version                # Versión de Python para UV
├── pyproject.toml                 # Configuración del proyecto y herramientas
├── uv.lock                        # Lock file de dependencias (reproducible)
└── README.md                      # Este archivo
```

## Requisitos

- Python >= 3.11 (gestionado automáticamente por UV)
- [UV](https://docs.astral.sh/uv/getting-started/installation/) - Gestor de paquetes y entornos virtuales
- MongoDB (local o en la nube) 

## Instalación

### 1. Instalar UV

Si aún no tienes UV instalado:

```bash
# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# O con pip
pip install uv
```

### 2. Clonar el repositorio

```bash
git clone <repository-url>
cd pdf-extractext
```

### 3. Crear entorno virtual e instalar dependencias

UV gestiona automáticamente el entorno virtual y las dependencias:

```bash
# Instalar todas las dependencias (incluye dev)
uv sync

# Solo dependencias de producción
uv sync --no-dev
```

Esto creará automáticamente el entorno virtual (`.venv`) e instalará todas las dependencias según el `uv.lock`.

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

**Variables importantes:**

```bash
# Aplicación
ENVIRONMENT=development
DEBUG=true
APP_NAME="PDF-ExtractExt"
APP_VERSION=0.1.0

# Servidor
HOST=0.0.0.0
PORT=8000

# MongoDB
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=pdf_extractext_db

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Uso

### Ejecutar el servidor de desarrollo

Con UV puedes ejecutar comandos sin activar manualmente el entorno virtual:

```bash
# Ejecutar uvicorn con recarga automática
uv run uvicorn src.interface.main:app --reload --host 0.0.0.0 --port 8000

# O usando el script configurado
uv run python -m src.interface.main
```

El comando `uv run` activa automáticamente el entorno virtual y ejecuta el comando dentro de él.

### Documentación de la API

Una vez iniciado el servidor, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check - Verifica estado del servicio |

## Testing

El proyecto utiliza **PyTest** con cobertura de código.

```bash
# Ejecutar todos los tests
uv run pytest

# Ejecutar con cobertura detallada
uv run pytest --cov=src --cov-report=term-missing --cov-report=html

# Ejecutar tests específicos
uv run pytest tests/domain/
uv run pytest tests/interface/test_health.py

# Ejecutar en modo verbose
uv run pytest -v
```

### Cobertura mínima

El proyecto está configurado para reportar cobertura. Puedes revisar el reporte HTML generado en `htmlcov/index.html`.

## Linting y Type Checking

### Ruff (Linter y Formateador)

```bash
# Verificar errores
uv run ruff check .

# Corregir errores automáticamente
uv run ruff check . --fix

# Formatear código
uv run ruff format .
```

### MyPy (Type Checker)

```bash
# Verificar tipos
uv run mypy src

# Verificar con informe detallado
uv run mypy src --show-error-codes
```

### Pre-commit (Opcional)

```bash
# Instalar hooks de pre-commit
uv run pre-commit install

# Ejecutar manualmente
uv run pre-commit run --all-files
```

## Comandos Útiles de UV

```bash
# Agregar nueva dependencia
uv add <package>

# Agregar dependencia de desarrollo
uv add --dev <package>

# Actualizar dependencias
uv sync --upgrade

# Ejecutar shell dentro del entorno
uv run bash

# Ver información del entorno
uv pip list
```
### Configuración de Entorno con Docker

Para este proyecto utilizamos **Docker** y **Docker Compose** para gestionar la base de datos MongoDB de forma aislada y persistente.

### 1. Instalación de Docker (en Fedora)
Si aún no tenés Docker, ejecutá estos comandos en tu terminal:

```bash
# Instalar dependencias y repo oficial
sudo dnf install dnf-plugins-core
sudo dnf config-manager --add-repo [https://download.docker.com/linux/fedora/docker-ce.repo](https://download.docker.com/linux/fedora/docker-ce.repo)

# Instalar motor de Docker y Compose
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Iniciar y habilitar el servicio
sudo systemctl start docker
sudo systemctl enable docker

# Opcional: Agregar tu usuario al grupo docker para no usar sudo (requiere reiniciar sesión)
# sudo usermod -aG docker $USER
```

## Flujo de Dependencias

```
Controller (Interface/API)
    ↓
Service (Application)
    ↓
Repository Interface (Domain) ← Repository Implementation (Infrastructure)
    ↓
Entity (Domain)
```

Esta estructura garantiza que:
- El dominio no depende de frameworks externos
- Las capas interiores son independientes
- Es fácil cambiar implementaciones (ej: cambiar MongoDB por PostgreSQL)
- El código es altamente testeable con mocks

## Licencia

MIT License - Ver archivo [LICENSE](LICENSE) para más detalles.

Copyright (c) 2026 MaJuVer

---

