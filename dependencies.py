from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlmodel import Session

from models.users import UserDB
from repositories.database import get_session
from services.jwt_service import JWTService

SessionDep = Annotated[Session, Depends(get_session)]

from repositories.user_repository import UserRepository  # noqa: E402

UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]

from services.user_service import UserService, UserServiceInterface  # noqa: E402

UserServiceDep = Annotated[UserServiceInterface, Depends(UserService)]

def get_jwt_service():
    return JWTService("my-secret-key")

JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]



from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # <-- AGREGADO

security = HTTPBearer() # <-- AGREGADO

def get_current_user(
    jwt_service: JWTServiceDep,
    repo: UserRepositoryDep,
    # authorization: Annotated[str | None, Header()] = None, # <-- ELIMINADO
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)] # <-- AGREGADO
) -> UserDB | None:
    # if not authorization or not authorization.startswith("Bearer "): # <-- ELIMINADO
    #     raise HTTPException(status_code=401, detail="Missing or invalid Authorization header") # <-- ELIMINADO
    #
    # token = authorization.removeprefix("Bearer ") # <-- ELIMINADO
    token = credentials.credentials # <-- AGREGADO
    payload = jwt_service.decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = repo.get_by_email(payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

CurrentUserDep = Annotated[UserDB, Depends(get_current_user)]
