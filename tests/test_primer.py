from fastapi.testclient import TestClient

from main import app # Importo variable "app"


cliente = TestClient(app)
def test_docs():
    respuesta = cliente.get("/docs")
    assert  respuesta.status_code == 200

# Chequear la seguridad
def test_no_logueado():
    respuesta = cliente.get("/user")
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Missing or invalid Authorization header"