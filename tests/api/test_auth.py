from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


def test_docs():
    respuesta = cliente.get("/docs")
    assert  respuesta.status_code == 200


# Login Ok
def test_login_ok():
    respuesta = cliente.post("/login", json= {
                                "email": "mgomez@email.com",
                                "password": "123"
                            })
    assert respuesta.status_code == 200
    assert respuesta.json()["msg"] == "ok"
    assert respuesta.json()["token"]


# Login Failed
def test_login_wrong_pwd():
    respuesta = cliente.post("/login", json= {
                                    "email": "mgomez@email.com",
                                    "password": "cualquiercontraseña"
                                })
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "User/password incorrect"


def test_login_wrong_email():
    respuesta = cliente.post("/login", json= {
                                    "email": "cualquieremail@email.com",
                                    "password": "cualquiercontraseña"
                                })
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "User/password incorrect"


def test_login_wrong_request():
    respuesta = cliente.post("/login", json= {
                                    "cualquiera": "cualquieremail@email.com"
                                    })
    assert respuesta.status_code == 422