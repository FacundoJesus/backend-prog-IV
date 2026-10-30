import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient
from sqlmodel import Session

from dependencies import get_current_user
from repositories.user_repository import UserRepository
from services.jwt_service import JWTService


def test_docs(client: TestClient) -> None:
    respuesta = client.get("/docs")
    assert respuesta.status_code == 200


# Login Ok
def test_login_ok(client: TestClient, seed: None) -> None:
    respuesta = client.post(
        "/login",
        json={
            "email": "mgomez@email.com",
            "password": "123",
        },
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["msg"] == "ok"
    assert respuesta.json()["token"]


# Login Failed
def test_login_wrong_pwd(client: TestClient, seed: None) -> None:
    respuesta = client.post(
        "/login",
        json={
            "email": "mgomez@email.com",
            "password": "cualquiercontraseña",
        },
    )
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "User/password incorrect"


def test_login_wrong_email(client: TestClient, seed: None) -> None:
    respuesta = client.post(
        "/login",
        json={
            "email": "cualquieremail@email.com",
            "password": "cualquiercontraseña",
        },
    )
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "User/password incorrect"


def test_login_wrong_request(client: TestClient) -> None:
    respuesta = client.post("/login", json={"cualquiera": "cualquieremail@email.com"})
    assert respuesta.status_code == 422


# Current User Helper
def test_get_current_user_helper(session: Session, seed: None) -> None:
    jwt_service = JWTService("my-secret-key")
    repo = UserRepository(session)
    valid_token = jwt_service.create_access_token({"sub": "mgomez@email.com"})

    # Éxito
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=valid_token)
    user = get_current_user(jwt_service, repo, creds)
    assert user.email == "mgomez@email.com"

    # Token inválido
    bad_creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="token_invalido")
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(jwt_service, repo, bad_creds)
    assert exc_info.value.status_code == 401

    # Usuario no encontrado
    ghost_token = jwt_service.create_access_token({"sub": "no_existe_en_bd@email.com"})
    ghost_creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=ghost_token)
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(jwt_service, repo, ghost_creds)
    assert exc_info.value.status_code == 401
