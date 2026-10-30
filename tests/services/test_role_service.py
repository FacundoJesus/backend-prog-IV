from sqlmodel import Session

from models.roles import RoleBase
from repositories.permission_repository import PermissionRepository
from repositories.role_repository import RoleRepository
from services.role_service import RoleService


def test_role_service_crud(session: Session, seed: None) -> None:
    service = RoleService(RoleRepository(session))

    # Get roles
    roles = service.get_roles(offset=0, limit=10)
    assert len(roles) >= 2

    # Create role
    new_role = service.create_role(RoleBase(name="MANAGER", description="Gestión"))
    assert new_role.id is not None
    assert new_role.name == "MANAGER"

    # Get by id & name
    found_id = service.get_role_by_id(new_role.id)
    assert found_id is not None and found_id.name == "MANAGER"

    found_name = service.get_role_by_name("MANAGER")
    assert found_name is not None and found_name.id == new_role.id

    # Update role
    updated = service.update_role(new_role.id, RoleBase(name="SENIOR_MANAGER", description="Líder"))
    assert updated is not None
    assert updated.name == "SENIOR_MANAGER"

    # Delete role
    service.delete_role(new_role.id)
    assert service.get_role_by_id(new_role.id) is None


def test_role_service_add_and_remove_permission(session: Session, seed: None) -> None:
    role_service = RoleService(RoleRepository(session))
    perm_repo = PermissionRepository(session)

    role = role_service.get_role_by_id(2)  # REGULAR
    assert role is not None

    permission = perm_repo.get_by_id(3)  # delete_users
    assert permission is not None

    # Agregar permiso
    role_service.add_permission(role, permission)
    assert any(p.id == 3 for p in role.permissions)

    # Remover permiso
    role_service.remove_permission(role, permission)
    assert not any(p.id == 3 for p in role.permissions)
