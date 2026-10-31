import pytest
from fastapi.testclient import TestClient


# Crear rol con datos válidos
def test_create_role_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    payload = {"name": "EDITOR", "description": "Rol de edición"}
    res = client.post("/role", json=payload, headers=admin_headers)
    assert res.status_code == 201
    assert "id" in res.json()


# Crear rol rechazado por nombre duplicado (409)
def test_create_role_duplicate(client: TestClient, admin_headers: dict[str, str]) -> None:
    # ADMIN ya existe por el seed
    payload = {"name": "ADMIN", "description": "Duplicado"}
    res = client.post("/role", json=payload, headers=admin_headers)
    assert res.status_code == 409
    assert res.json()["detail"] == "Role already exists"


# Obtener listado de roles
def test_get_roles_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/role", headers=admin_headers)
    assert res.status_code == 200
    roles = res.json()
    assert len(roles) >= 2  # ADMIN y REGULAR del seed


# Obtener listado de roles con paginación
def test_get_roles_pagination(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/role?offset=0&limit=1", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1


# Obtener rol por ID existente
def test_get_role_by_id_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/role/1", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert data["name"] == "ADMIN"
    assert "permissions" in data


# Obtener rol por ID inexistente (404)
def test_get_role_by_id_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/role/999", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Role not found"


# Actualizar datos de un rol existente
def test_update_role_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    payload = {"name": "REGULAR_MODIFICADO", "description": "Nueva descripcion"}
    res = client.patch("/role/2", json=payload, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["id"] == 2


# Actualizar rol inexistente (404)
def test_update_role_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    payload = {"name": "X", "description": "Y"}
    res = client.patch("/role/999", json=payload, headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Role not found"


# Actualizar rol rechazado por conflicto de nombre duplicado (409)
def test_update_role_duplicate_name(client: TestClient, admin_headers: dict[str, str]) -> None:
    # Intentar cambiar el nombre del rol 2 al nombre del rol 1 ("ADMIN")
    payload = {"name": "ADMIN", "description": "Conflicto"}
    res = client.patch("/role/2", json=payload, headers=admin_headers)
    assert res.status_code == 409
    assert res.json()["detail"] == "Role already exists"


# Eliminar rol existente con éxito
def test_delete_role_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    # Creamos un rol para borrar
    create_res = client.post("/role", json={"name": "BORRABLE", "description": "Borrar"}, headers=admin_headers)
    role_id = create_res.json()["id"]

    res = client.delete(f"/role/{role_id}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["msg"] == "Rol borrado con éxito"

    # Verificar que ya no existe
    res_check = client.get(f"/role/{role_id}", headers=admin_headers)
    assert res_check.status_code == 404


# Eliminar rol inexistente (404)
def test_delete_role_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.delete("/role/999", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Role not found"


# Asignar y desasignar permiso a un rol exitosamente
def test_add_and_remove_permission_to_role_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    # Permiso 3 (delete_users) al rol 2 (REGULAR)
    res_add = client.post("/role/2/permission/3", headers=admin_headers)
    assert res_add.status_code == 200
    assert any(p["id"] == 3 for p in res_add.json()["permissions"])

    # Remover permiso 3 del rol 2
    res_del = client.delete("/role/2/permission/3", headers=admin_headers)
    assert res_del.status_code == 200
    assert not any(p["id"] == 3 for p in res_del.json()["permissions"])


# Asignar permiso fallido por rol inexistente (404)
def test_add_permission_role_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.post("/role/999/permission/1", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Role not found"


# Asignar permiso inexistente a un rol (404)
def test_add_permission_permission_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.post("/role/1/permission/999", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Permission not found"


# Desasignar permiso fallido por rol inexistente (404)
def test_remove_permission_role_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.delete("/role/999/permission/1", headers=admin_headers)
    assert res.status_code == 404


# Desasignar permiso inexistente de un rol (404)
def test_remove_permission_permission_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.delete("/role/1/permission/999", headers=admin_headers)
    assert res.status_code == 404


# Obtener usuarios asociados a un rol existente
def test_get_role_users_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/role/1/user", headers=admin_headers)
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 1
    assert any(u["id"] == 1 for u in users)


# Obtener usuarios de un rol inexistente (404)
def test_get_role_users_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/role/999/user", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Role not found"


# Verificar protección de endpoints de roles sin token de autenticación (401)
@pytest.mark.parametrize(
    "method, path",
    [
        ("get", "/role"),
        ("get", "/role/1"),
        ("post", "/role"),
        ("patch", "/role/1"),
        ("delete", "/role/1"),
        ("get", "/role/1/user"),
    ],
)
def test_roles_protegidos_sin_auth(client: TestClient, method: str, path: str) -> None:
    res = getattr(client, method)(path)
    assert res.status_code == 401
