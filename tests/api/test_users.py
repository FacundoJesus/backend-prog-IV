import pytest
from fastapi.testclient import TestClient


# Obtener listado general de usuarios
def test_get_user_ok(client: TestClient, auth_headers: dict[str, str]) -> None:
    res = client.get("/user", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 3


# Obtener listado de usuarios con paginación
def test_get_users_pagination(client: TestClient, auth_headers: dict[str, str]) -> None:
    res = client.get("/user?offset=1&limit=1", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1


# Crear un nuevo usuario con datos válidos
def test_create_user_ok(client: TestClient, auth_headers: dict[str, str]) -> None:
    payload = {
        "name": "Nuevo Usuario",
        "email": "nuevo@email.com",
        "age": 25,
        "password": "password123",
        "country_id": 1,
    }
    res = client.post("/user", json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert data["id"] is not None


# Creación de usuario rechazada por datos inválidos (422)
def test_create_user_invalid(client: TestClient, auth_headers: dict[str, str]) -> None:
    payload = {
        "name": "Test",
        "email": "test_invalid@email.com",
        "age": "no_es_un_numero",
        "password": "password123",
        "country_id": 1,
    }
    res = client.post("/user", json=payload, headers=auth_headers)
    assert res.status_code == 422


# Creación de usuario rechazada por falta de permisos (403)
def test_create_user_forbidden(client: TestClient, regular_headers: dict[str, str]) -> None:
    payload = {
        "name": "Nuevo Usuario",
        "email": "nuevo@email.com",
        "age": 25,
        "password": "password123",
        "country_id": 1,
    }
    res = client.post("/user", json=payload, headers=regular_headers)
    assert res.status_code == 403
    assert "Missing permission" in res.json()["detail"]


# Obtener usuario por ID existente
def test_get_user_by_id_ok(client: TestClient, auth_headers: dict[str, str]) -> None:
    res = client.get("/user/1", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["id"] == 1
    assert res.json()["email"] == "mgomez@email.com"
    assert "country" in res.json()


# Obtener usuario por ID inexistente (404)
def test_get_user_by_id_fail(client: TestClient, auth_headers: dict[str, str]) -> None:
    res = client.get("/user/120", headers=auth_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"


# Buscar usuarios por coincidencia de nombre
def test_search_user_ok(client: TestClient, auth_headers: dict[str, str]) -> None:
    res = client.get("/user/search/Martina", headers=auth_headers)
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 1
    assert any("Martina" in u["name"] for u in users)


# Buscar usuarios sin coincidencias
def test_search_user_empty(client: TestClient, auth_headers: dict[str, str]) -> None:
    res = client.get("/user/search/InexistenteXYZ", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []


# Obtener ID del usuario actualmente autenticado
def test_get_my_id_ok(client: TestClient, auth_headers: dict[str, str]) -> None:
    res = client.get("/user/me/id", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == {"id": 1}


# Obtener usuarios mayores de edad
def test_search_mayores_ok(client: TestClient, auth_headers: dict[str, str]) -> None:
    res = client.get("/user_mayores", headers=auth_headers)
    assert res.status_code == 200
    users = res.json()
    assert len(users) == 2  # Martina (28) y Santiago (34), Camila (15) no debe estar
    assert all(u["age"] >= 18 for u in users)


# Actualizar datos de un usuario existente
def test_update_user_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    update_data = {
        "name": "Santiago Modificado",
        "email": "sfer@email.com",
        "password": "password123",
        "age": 35,
        "country_id": 1,
    }
    res = client.patch("/user/2", json=update_data, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["id"] == 2


# Actualizar usuario inexistente (404)
def test_update_user_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    update_data = {
        "name": "No Existe",
        "email": "noexiste@email.com",
        "password": "password123",
        "age": 40,
        "country_id": 1,
    }
    res = client.patch("/user/999", json=update_data, headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"


# Actualizar usuario rechazado por falta de permisos (403)
def test_update_user_forbidden(client: TestClient, regular_headers: dict[str, str]) -> None:
    update_data = {
        "name": "Intento Modificar",
        "email": "sfer@email.com",
        "password": "password123",
        "age": 35,
        "country_id": 1,
    }
    res = client.patch("/user/2", json=update_data, headers=regular_headers)
    assert res.status_code == 403
    assert "Missing permission" in res.json()["detail"]


# Eliminar usuario rechazado por falta de permisos (403)
def test_delete_user_forbidden(client: TestClient, regular_headers: dict[str, str]) -> None:
    res = client.delete("/user/3", headers=regular_headers)
    assert res.status_code == 403
    assert "Missing permission" in res.json()["detail"]


# Eliminar usuario existente con éxito
def test_delete_user_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.delete("/user/3", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["msg"] == "Usuario borrado con éxito"

    # Verificar que ya no existe
    res_check = client.get("/user/3", headers=admin_headers)
    assert res_check.status_code == 404


# Eliminar usuario inexistente (404)
def test_delete_user_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.delete("/user/999", headers=admin_headers)
    assert res.status_code == 404


# Asignar y desasignar rol a un usuario exitosamente
def test_add_and_remove_role_to_user_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    res_add = client.post("/user/2/role/1", headers=admin_headers)
    assert res_add.status_code == 200

    res_del = client.delete("/user/2/role/1", headers=admin_headers)
    assert res_del.status_code == 200


# Asignar rol a usuario rechazado por falta de permisos (403)
def test_add_role_forbidden_for_regular(client: TestClient, regular_headers: dict[str, str]) -> None:
    res = client.post("/user/2/role/1", headers=regular_headers)
    assert res.status_code == 403
    assert "Missing permission" in res.json()["detail"]


# Desasignar rol a usuario rechazado por falta de permisos (403)
def test_remove_role_forbidden_for_regular(client: TestClient, regular_headers: dict[str, str]) -> None:
    res = client.delete("/user/2/role/1", headers=regular_headers)
    assert res.status_code == 403
    assert "Missing permission" in res.json()["detail"]


# Asignar rol fallido por usuario inexistente (404)
def test_add_role_user_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.post("/user/999/role/1", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"


# Asignar rol inexistente a un usuario (404)
def test_add_role_role_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.post("/user/1/role/999", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Role not found"


# Desasignar rol fallido por usuario inexistente (404)
def test_remove_role_user_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.delete("/user/999/role/1", headers=admin_headers)
    assert res.status_code == 404


# Desasignar rol inexistente de un usuario (404)
def test_remove_role_role_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.delete("/user/1/role/999", headers=admin_headers)
    assert res.status_code == 404


# Verificar protección de endpoints de usuarios sin token de autenticación (401)
@pytest.mark.parametrize(
    "method, path",
    [
        ("get", "/user"),
        ("get", "/user/1"),
        ("get", "/user/search/ma"),
        ("get", "/user_mayores"),
        ("get", "/user/me/id"),
        ("post", "/user"),
        ("patch", "/user/1"),
        ("delete", "/user/1"),
    ],
)
def test_protegidos(client: TestClient, method: str, path: str) -> None:
    res = getattr(client, method)(path)
    assert res.status_code == 401
    assert res.json()["detail"] == "Missing or invalid Authorization header"
