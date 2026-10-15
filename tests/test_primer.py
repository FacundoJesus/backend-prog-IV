from fastapi.testclient import TestClient

from main import app # Importo variable "app"

cliente = TestClient(app)


def test_docs():
    respuesta = cliente.get("/docs")
    assert  respuesta.status_code == 200



# Login NOT
def test_no_logueado():
    respuesta = cliente.get("/user")
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Missing or invalid Authorization header"



# Login OK
def test_login_ok():
    respuesta = cliente.post("/login", json= {
                                "email": "mgomez@email.com",
                                "password": "123"
                            })
    assert respuesta.status_code == 200
    assert respuesta.json()["msg"] == "ok"
    assert respuesta.json()["token"]



# Crear usuario OK
def test_create_user_ok():
    # 1. Nos logueamos con un usuario existente para obtener un token válido
    login_resp = cliente.post("/login", json={
        "email": "mgomez@email.com",
        "password": "123"
    })
    token = login_resp.json()["token"]

    # 2. Hacemos el POST enviando el token en los headers
    resp = cliente.post(
        "/user",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Facundo",
            "age": 29,
            "country_id": 1,
            "email": "facucitera@hotmail.com",
            "password": "pass123",
        },
    )
    # 3. Verificamos el código 200 y que retorne el id del nuevo usuario
    assert resp.status_code == 200
    assert "id" in resp.json()



# Obtener usuarios OK
def test_get_users_ok():
    # 1. Nos logueamos con un usuario existente para obtener un token válido
    login_resp = cliente.post("/login", json={
        "email": "mgomez@email.com",
        "password": "123"
    })
    token = login_resp.json()["token"]

    # 2. Hacemos la petición GET enviando el token en los headers
    resp = cliente.get("/user?limit=2&offset=0", headers={"Authorization": f"Bearer {token}"})

    # 3. Verificamos código 200 y que devuelva una lista con la estructura esperada
    assert resp.status_code == 200
    usuarios = resp.json()
    assert isinstance(usuarios, list)
    assert len(resp.json()) == 2
    # Validamos que cada usuario contenga los campos de GetUsersResponse (id y name)
    assert "id" in usuarios[0]
    assert "name" in usuarios[0]

