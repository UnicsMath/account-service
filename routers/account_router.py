from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from controllers.account.iaccount_controller import IAccountController
from controllers.account.account_controller import AccountController

from repository.account.account_repository import AccountRepository

from schemas.token_schema import TokenSchema
from utilities.db_session import get_db

controller: IAccountController = AccountController(AccountRepository())

router = APIRouter()


@router.post("/authentication", response_model=TokenSchema)
async def authentication(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> TokenSchema:
    token_schema = controller.authentication(form_data, db)
    return token_schema
