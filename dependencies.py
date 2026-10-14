from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlmodel import Session
from models.users import UserDB
from repositories.database import get_session
from services.jwt_service import JWTService

# Para obtener la sesion
SessionDep = Annotated[Session, Depends(get_session)]

from repositories.user_repository import UserRepository
# Para usarlo en user_service
UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]


from services.user_service import UserService, UserServiceInterface
# Para usarlo en user_controller
UserServiceDep = Annotated[UserServiceInterface, Depends(UserService)]

def get_jwt_service():
    return JWTService("my-secret-key")
# Para usarlo en login_controller
JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(
    jwt_service: JWTServiceDep,
    repo: UserRepositoryDep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> UserDB | None:
    token = credentials.credentials
    payload = jwt_service.decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = repo.get_by_email(payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

CurrentUserDep = Annotated[UserDB, Depends(get_current_user)]

def get_current_user_id(request: Request, repo: UserRepositoryDep) -> int:
    # The JWT was already validated by JWTAuthMW, which stores the payload in request.state.
    payload = getattr(request.state, "jwt_payload", None)
    if payload is None:
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    user = repo.get_by_email(payload["sub"])
    if not user or user.id is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user.id

CurrentUserIdDep = Annotated[int, Depends(get_current_user_id)]