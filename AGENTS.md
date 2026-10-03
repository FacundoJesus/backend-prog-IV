# backend-prog-IV
Backend desarrollado para la cátedra de Programación IV de la UTN Paraná. Expone una API RESTful para la gestión de usuarios y autenticación.

## Stack
- Lenguaje: Python 3
- Framework: FastAPI
- Servidor ASGI: Uvicorn
- Base de datos: SQLite usando SQLModel (SQLAlchemy)
- Autenticación: JWT (PyJWT) y bcrypt (encriptación de contraseñas)
- Linter/Formatter: Ruff (configurado en `pyproject.toml`)
- Type Checker: Pyright

## Comandos
- `fastapi dev main.py` — arranca el servidor en local con recarga en caliente (hot-reload).
- `ruff check .` — revisa el estilo y posibles errores en el código (linter).
- `pytest` — ejecuta los tests (si se encuentran configurados en el futuro).

## Estructura del proyecto
- `api/` — Endpoints y rutas de FastAPI (controladores). Contiene también middlewares.
- `models/` — Modelos de datos (SQLModel) y esquemas de validación (Pydantic).
- `repositories/` — Acceso a datos, configuración de la BD e interacciones directas con la base de datos (Patrón Repository).
- `services/` — Lógica de negocio (ej. manejo de login, JWT, y operaciones sobre usuarios).
- `utils/` — Funciones utilitarias auxiliares (como el manejo de hashes y passwords).
- `dependencies.py` — Dependencias inyectables compartidas por la API (ej. obtención del usuario actual).

## Convenciones
- **Estilo de código:** Seguir PEP 8. Variables y funciones en `snake_case`, clases en `PascalCase`.
- **Typing:** Uso obligatorio y estricto de _type hints_ (anotaciones de tipo) en parámetros y retornos de funciones, validables con Pyright.
- **Inyección de Dependencias:** Favorecer el uso de `Depends()` de FastAPI para separar la lógica de infraestructura (como conexiones a la BD o servicios) de los endpoints.
- **Base de datos:** Manejar las sesiones a través de SQLModel y mantener la lógica de consultas SQL estrictamente dentro de la capa `repositories/`.

## No hagas
- No instalar dependencias o actualizar versiones sin justificación, en especial aquellas sensibles como `bcrypt` que requieran un entorno de compilación complejo (C/C++).
- No hardcodear tokens, secrets, o credenciales (excepto `my-secret-key` provisto para fines de desarrollo).
- No subir archivos sensibles al repositorio como `database.db` o la carpeta de entorno virtual `.venv`.
- No alterar las importaciones y estructura en `main.py` sin asegurarse de que no se rompe el flujo de inicialización y carga de datos de prueba.

## Flujo de trabajo
- Antes de una tarea no trivial o que implique cambios arquitectónicos, propón un plan y espera mi OK.
- Una tarea a la vez; al terminar, dime qué cambiaste para que lo revise.
- Si no estás seguro al 80%, pregunta. No inventes.

## Documentación
- Referencias principales: Documentación oficial de [FastAPI](https://fastapi.tiangolo.com/) y [SQLModel](https://sqlmodel.tiangolo.com/).
