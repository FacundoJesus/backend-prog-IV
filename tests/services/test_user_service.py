from sqlmodel import Session

from models.roles import Role
from models.users import User
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from services.user_service import UserService


# Obtener listado de usuarios desde la capa de servicio
def test_user_service_get_users(session: Session, seed: None) -> None:
    service = UserService(UserRepository(session))
    users = service.get_users(offset=0, limit=10)
    assert len(users) == 3


# Creación de usuario con contraseña hasheada en servicio
def test_user_service_create_user(session: Session, seed: None) -> None:
    service = UserService(UserRepository(session))
    new_user = User(
        name="Carlos Perez",
        email="cperez@email.com",
        age=30,
        password="password123",
        country_id=1,
    )
    created = service.create_user(new_user)
    assert created.id is not None
    assert created.email == "cperez@email.com"


# Obtención de usuario por ID en servicio (existente e inexistente)
def test_user_service_get_by_id(session: Session, seed: None) -> None:
    service = UserService(UserRepository(session))
    user = service.get_user_by_id(1)
    assert user is not None
    assert user.name == "Martina Gómez"

    user_none = service.get_user_by_id(999)
    assert user_none is None


# Búsqueda de usuarios por coincidencia de nombre en servicio
def test_user_service_search_users(session: Session, seed: None) -> None:
    service = UserService(UserRepository(session))
    results = service.search_users("Martina")
    assert len(results) == 1
    assert results[0].email == "mgomez@email.com"


# Filtrado de usuarios mayores de edad en servicio
def test_user_service_search_mayores(session: Session, seed: None) -> None:
    service = UserService(UserRepository(session))
    adults = service.search_mayores()
    assert len(adults) == 2
    assert all(u.age >= 18 for u in adults)


# Actualización de datos de usuario en servicio (existente e inexistente)
def test_user_service_update_user(session: Session, seed: None) -> None:
    service = UserService(UserRepository(session))
    user_update = User(
        name="Martina Actualizada",
        email="mgomez@email.com",
        age=29,
        password="password123",
        country_id=1,
    )
    updated = service.update_user(1, user_update)
    assert updated is not None
    assert updated.name == "Martina Actualizada"
    assert updated.age == 29

    updated_none = service.update_user(999, user_update)
    assert updated_none is None


# Eliminación de usuario en la capa de servicio
def test_user_service_delete_user(session: Session, seed: None) -> None:
    service = UserService(UserRepository(session))
    service.delete_user(3)
    assert service.get_user_by_id(3) is None


# Asignación y desasignación de roles a un usuario en servicio
def test_user_service_add_and_remove_role(session: Session, seed: None) -> None:
    user_service = UserService(UserRepository(session))
    role_repo = RoleRepository(session)

    user = user_service.get_user_by_id(2)
    assert user is not None

    role = role_repo.get_by_id(1)  # ADMIN
    assert role is not None

    # Asignar rol
    user_service.add_role(user, role)
    assert any(r.id == 1 for r in user.roles)

    # Remover rol
    user_service.remove_role(user, role)
    assert not any(r.id == 1 for r in user.roles)
