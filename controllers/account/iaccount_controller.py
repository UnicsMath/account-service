from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from repository.account.iaccount_repository import IAccountRepository
from schemas.account_schema import AccountBaseSchema
from schemas.token_schema import TokenSchema


class IAccountController(ABC):
    @abstractmethod
    def __init__(self, account_repository: IAccountRepository):
        self.__account_repository: IAccountRepository = account_repository

    @abstractmethod
    def authentication(
        self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session
    ) -> TokenSchema:
        pass

    @abstractmethod
    def authorization(self, decoded_jwt: dict, db: Session) -> AccountBaseSchema:
        pass
