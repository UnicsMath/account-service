from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from models.account_model import AccountModel


class IAccountRepository(ABC):
    @abstractmethod
    def get_by_email(self, db: Session, email: str) -> AccountModel:
        pass

    @abstractmethod
    def get_by_username(self, db: Session, username: str) -> AccountModel:
        pass
