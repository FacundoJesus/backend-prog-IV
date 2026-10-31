from utils.hash import hash_password, verify_password


# Generación de hash bcrypt y verificación de contraseñas
def test_hash_password_and_verify() -> None:
    raw = "mi_contraseña_secreta"
    hashed = hash_password(raw)

    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("otra_contraseña", hashed) is False
