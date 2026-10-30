from sqlmodel import Session

from repositories.user_repository import UserRepository
from services.login_service import LoginService


def test_login_success(session: Session, seed: None) -> None:
    repo = UserRepository(session)
    service = LoginService(repo)
    assert service.login("mgomez@email.com", "123") is True


def test_login_wrong_password(session: Session, seed: None) -> None:
    repo = UserRepository(session)
    service = LoginService(repo)
    assert service.login("mgomez@email.com", "clave_erronea") is False


def test_login_user_not_found(session: Session, seed: None) -> None:
    repo = UserRepository(session)
    service = LoginService(repo)
    assert service.login("no_existe@email.com", "123") is False
