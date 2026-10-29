# backend-prog-IV
Backend desarrollado para la cátedra de Programación IV de la UTN Paraná. Expone una API RESTful para la gestión de usuarios, autenticación y autorización mediante roles y permisos (RBAC).

## Stack
- Lenguaje: Python 3
- Framework: FastAPI
- Servidor ASGI: Uvicorn
- Base de datos: SQLite usando SQLModel (SQLAlchemy)
- Autenticación y Autorización: JWT (PyJWT), bcrypt (encriptación de contraseñas) y control de acceso basado en roles y permisos (RBAC)
- Linter/Formatter: Ruff (configurado en `pyproject.toml`)
- Type Checker: Pyright

## Comandos
- `fastapi dev main.py` — arranca el servidor en local con recarga en caliente (hot-reload).
- `ruff check .` — revisa el estilo y posibles errores en el código (linter).
- `pytest` — ejecuta los tests del proyecto (pruebas unitarias y de integración).
- `/code-review` — analiza y audita el código del proyecto en busca de errores, tipado y respeto de capas.

## Estructura del proyecto
- `api/` — Endpoints y rutas de FastAPI (controladores: usuarios, login, roles, permisos). Contiene middlewares (`auth`, `counter`) y decoradores de protección (`@protected`).
- `api/payload/` — Esquemas de validación y DTOs de request/response (usuarios, roles, permisos).
- `models/` — Modelos de datos (SQLModel) para usuarios (`users.py`), permisos (`permissions.py`) y roles (`roles.py`, con tablas intermedias `RolePermission` y `UserRole`).
- `repositories/` — Acceso a datos, configuración de la BD e interacciones directas con la base de datos (Patrón Repository: usuarios, roles, permisos) y semillas de datos (`seed.py`).
- `services/` — Lógica de negocio e interfaces abstractas (`UserServiceInterface`, `RoleServiceInterface`, `PermissionServiceInterface`, `JWTService`).
- `utils/` — Funciones utilitarias auxiliares (como el manejo de hashes y contraseñas).
- `dependencies.py` — Dependencias inyectables compartidas por la API (sesión de BD, repositorios, interfaces de servicios, autenticación y usuario actual).
- `tests/` — Tests automatizados unitarios y de integración con `pytest` (`tests/api/`, `tests/services/`).

## Convenciones
- **Estilo de código:** Seguir PEP 8. Variables y funciones en `snake_case`, clases en `PascalCase`.
- **Typing:** Uso obligatorio y estricto de _type hints_ (anotaciones de tipo) en parámetros y retornos de funciones, validables con Pyright.
- **Inyección de Dependencias e Interfaces:** Favorecer el uso de `Depends()` de FastAPI. Los servicios deben definir e implementar interfaces abstractas (`ABC`) inyectadas como dependencias tipadas en los controladores.
- **Base de datos y Relaciones:** Manejar las sesiones a través de SQLModel y mantener la lógica de consultas SQL estrictamente dentro de la capa `repositories/`. Las relaciones muchos a muchos (`User`-`Role`, `Role`-`Permission`) se definen mediante tablas intermedias con `link_model`.
- **Seguridad y Protección de Endpoints:** Uso del decorador `@protected` y esquemas de autenticación (`HTTPBearer`) para endpoints restringidos.

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
