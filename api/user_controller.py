from typing import Annotated, Sequence

from fastapi import APIRouter, HTTPException, Query

from api.payload.user_dto import (
    CreateUserRequest,
    CreateUserResponse,
    DeleteUserResponse,
    GetUserResponseWithCountry,
    GetUsersResponse,
)
from dependencies import CurrentUserDep, UserServiceDep
from models.users import User, UserDB


router = APIRouter(tags=["Users"])

# Crear usuario
@router.post("/user", response_model=CreateUserResponse)
def create_user(req: CreateUserRequest, service: UserServiceDep) -> User:
    user = User(name=req.name, age=req.age, email=req.email, password=req.password, country_id=req.country_id)
    return service.create_user(user)

# Obtener usuarios
@router.get("/user", response_model=Sequence[GetUsersResponse])
def get_users_endpoint(
    service: UserServiceDep,
    me: CurrentUserDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
)-> Sequence[User]:
    print(f"soy el usuario {me}")
    return service.get_users(offset, limit)
    

# Obtener usuario por id
@router.get("/user/{user_id}", response_model=GetUserResponseWithCountry)
def get_user_by_id(user_id: int, service: UserServiceDep) -> UserDB:
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Obtener usuario por nombre
@router.get("/user/search/{name}")
def search_user(name: str, service: UserServiceDep) -> Sequence[UserDB]:
    return service.search_users(name)

# Obtener usuarios mayores
@router.get("/user_mayores")
def search_mayores(service: UserServiceDep)-> Sequence[UserDB]:
    return service.search_mayores()

# Eliminar usuario por id
@router.delete("/user/{user_id}", response_model=DeleteUserResponse)
def delete_user(user_id: int, service: UserServiceDep) -> DeleteUserResponse:
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    service.delete_user(user_id)
    return DeleteUserResponse(msg='Usuario borrado con éxito')

# Actualizar usuario por id
@router.patch("/user/{user_id}", response_model=CreateUserResponse)
def update_user(user_id: int, req: CreateUserRequest, service: UserServiceDep) -> UserDB | None:
    user = User(name=req.name, email=req.email, password=req.password, age=req.age, country_id=req.country_id)
    res = service.update_user(user_id, user)
    if res:
        return res
    raise HTTPException(status_code=404, detail="User not found")
