from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from models.roles import RolePermission

if TYPE_CHECKING:
    from models.roles import Role


class PermissionBase(SQLModel):
    name: str = Field(unique=True, index=True)
    description: str | None = None


class Permission(PermissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    roles: list["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)
