from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status

from controllers.account.iaccount_controller import (
    IAccountController,
    IAccountRepository,
    Depends,
    OAuth2PasswordRequestForm,
    Session,
    Annotated,
    TokenSchema,
)

from models.account_model import AccountModel

from utilities.security import (
    verify_hashes,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


class AccountController(IAccountController):
    def __init__(self, account_repository: IAccountRepository):
        super().__init__(account_repository)
        self.__account_repository: IAccountRepository = account_repository

    def authentication(
        self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session
    ) -> TokenSchema:
        user = self.__authenticate_account(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token: str = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return TokenSchema(access_token=access_token, token_type="bearer")

    def __authenticate_account(
        self, email: str, password: str, db: Session
    ) -> Optional[AccountModel]:
        user = self.__account_repository.get_by_email(db, email)
        if not user:
            return None
        if not verify_hashes(password, user.hashed_passcode):
            return None
        return user
