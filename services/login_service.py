from abc import ABC, abstractmethod

from dependencies import UserRepositoryDep
from utils.hash import verify_password


class LoginServiceInterface(ABC):
    @abstractmethod
    def login(self, email: str, pwd: str) -> bool: ...


class LoginService(LoginServiceInterface):
    def __init__(self, repo: UserRepositoryDep) -> None:
        self.repo = repo

    def login(self, email: str, pwd: str) -> bool:
        user = self.repo.get_by_email(email)
        if not user:
            return False
        return verify_password(pwd, user.password)
    