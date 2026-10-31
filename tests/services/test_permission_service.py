from sqlmodel import Session

from models.permissions import PermissionBase
from repositories.permission_repository import PermissionRepository
from services.permission_service import PermissionService


# Operaciones CRUD completas en el servicio de permisos
def test_permission_service_crud(session: Session, seed: None) -> None:
    service = PermissionService(PermissionRepository(session))

    # Get permissions
    perms = service.get_permissions(offset=0, limit=10)
    assert len(perms) >= 4

    # Create permission
    new_perm = service.create_permission(PermissionBase(name="audit_logs", description="Auditar logs"))
    assert new_perm.id is not None
    assert new_perm.name == "audit_logs"

    # Get by id & name
    found_id = service.get_permission_by_id(new_perm.id)
    assert found_id is not None and found_id.name == "audit_logs"

    found_name = service.get_permission_by_name("audit_logs")
    assert found_name is not None and found_name.id == new_perm.id

    # Update permission
    updated = service.update_permission(new_perm.id, PermissionBase(name="view_audit_logs", description="Ver logs"))
    assert updated is not None
    assert updated.name == "view_audit_logs"

    # Delete permission
    service.delete_permission(new_perm.id)
    assert service.get_permission_by_id(new_perm.id) is None
