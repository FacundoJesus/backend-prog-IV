import pytest
from fastapi.testclient import TestClient


# CREATE PERMISSION
def test_create_permission_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    payload = {"name": "export_reports", "description": "Permiso para exportar reportes"}
    res = client.post("/permission", json=payload, headers=admin_headers)
    assert res.status_code == 201
    assert "id" in res.json()


def test_create_permission_duplicate(client: TestClient, admin_headers: dict[str, str]) -> None:
    # "read_users" ya existe por el seed
    payload = {"name": "read_users", "description": "Duplicado"}
    res = client.post("/permission", json=payload, headers=admin_headers)
    assert res.status_code == 409
    assert res.json()["detail"] == "Permission already exists"


# GET PERMISSIONS
def test_get_permissions_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/permission", headers=admin_headers)
    assert res.status_code == 200
    perms = res.json()
    assert len(perms) >= 4  # 4 permisos del seed


def test_get_permissions_pagination(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/permission?offset=0&limit=2", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.json()) == 2


# GET PERMISSION BY ID
def test_get_permission_by_id_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/permission/1", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert "name" in data


def test_get_permission_by_id_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.get("/permission/999", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Permission not found"


# UPDATE PERMISSION
def test_update_permission_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    payload = {"name": "write_users_modificado", "description": "Permiso modificado"}
    res = client.patch("/permission/1", json=payload, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["id"] == 1


def test_update_permission_duplicate(client: TestClient, admin_headers: dict[str, str]) -> None:
    # Intentar renombrar el permiso 1 al nombre del permiso 2 ("read_users")
    payload = {"name": "read_users", "description": "Conflicto"}
    res = client.patch("/permission/1", json=payload, headers=admin_headers)
    assert res.status_code == 409
    assert res.json()["detail"] == "Permission already exists"


def test_update_permission_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    payload = {"name": "no_existe", "description": "Desc"}
    res = client.patch("/permission/999", json=payload, headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Permission not found"


# DELETE PERMISSION
def test_delete_permission_ok(client: TestClient, admin_headers: dict[str, str]) -> None:
    # Creamos un permiso para borrar
    create_res = client.post(
        "/permission",
        json={"name": "permiso_borrable", "description": "Para borrar"},
        headers=admin_headers,
    )
    perm_id = create_res.json()["id"]

    res = client.delete(f"/permission/{perm_id}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["msg"] == "Permiso borrado con éxito"

    # Verificar que ya no existe
    res_check = client.get(f"/permission/{perm_id}", headers=admin_headers)
    assert res_check.status_code == 404


def test_delete_permission_not_found(client: TestClient, admin_headers: dict[str, str]) -> None:
    res = client.delete("/permission/999", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Permission not found"


# PROTECTED ROUTES
@pytest.mark.parametrize(
    "method, path",
    [
        ("get", "/permission"),
        ("get", "/permission/1"),
        ("post", "/permission"),
        ("patch", "/permission/1"),
        ("delete", "/permission/1"),
    ],
)

def test_permissions_protegidos_sin_auth(client: TestClient, method: str, path: str) -> None:
    res = getattr(client, method)(path)
    assert res.status_code == 401
