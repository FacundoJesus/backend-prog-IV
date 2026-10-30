from services.jwt_service import JWTService


def test_init() -> None:
    jwt_service = JWTService("my-secret")
    assert jwt_service.algorithm == "HS256"
    assert jwt_service.expire_minutes == 30


def test_create_and_decode_token_ok() -> None:
    jwt_service = JWTService("secret-key-32-chars-long-test-pass", expire_minutes=15)
    token = jwt_service.create_access_token({"sub": "usuario@test.com", "role": "admin"})
    assert isinstance(token, str)

    payload = jwt_service.decode_token(token)
    assert payload is not None
    assert payload["sub"] == "usuario@test.com"
    assert payload["role"] == "admin"
    assert "exp" in payload


def test_decode_expired_token() -> None:
    # expire_minutes negativo para generar un token inmediatamente expirado
    jwt_service = JWTService("secret-key-32-chars-long-test-pass", expire_minutes=-5)
    token = jwt_service.create_access_token({"sub": "expirado@test.com"})

    payload = jwt_service.decode_token(token)
    assert payload is None


def test_decode_invalid_token() -> None:
    jwt_service = JWTService("secret-key-32-chars-long-test-pass")
    payload = jwt_service.decode_token("token_completamente_invalido_xyz")
    assert payload is None


def test_decode_wrong_secret() -> None:
    service1 = JWTService("secret-key-111111111111111111111111")
    service2 = JWTService("secret-key-222222222222222222222222")

    token = service1.create_access_token({"sub": "test@test.com"})
    payload = service2.decode_token(token)
    assert payload is None
