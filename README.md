#README

# Proyecto
Extraer texto de un pdf que es proporcionado por el usuario. Después se hae un resumen gracias a a un modelo de IA.

## Tecnologias:
* Python
* UV
* Modelo de Ia (a definir)
* Ollama
* xD
* Base de datos no relacional MongoDB

## Metodologias:
* TDD
* Proyecto dirigido en GitHub
* CC los seis primeros principios de 12 factor_APP

## Principios de programación:
* KISS
* DRY
* YAGNI
* SOLID

## Como levantar el entorno:
1.copia el archivo '.env.example' a '.env' y completa con tus datos.
2. Ejecuta 'uv sync' para las dependecias de Python.
3. Levanta la DB con 'docker compose up -d'.
4. Corre los tests con 'uv run pytest'.
