from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from controllers.account.account_controller import AccountController
from controllers.account.iaccount_controller import IAccountController
from repository.account.account_repository import AccountRepository
from schemas.account_schema import AccountBaseSchema
from schemas.token_schema import TokenSchema
from utilities.db_session import get_db
from utilities.security import decode_access_token

controller: IAccountController = AccountController(AccountRepository())

router = APIRouter()


@router.post("/authentication", response_model=TokenSchema)
async def authentication(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> TokenSchema:
    token_schema = controller.authentication(form_data, db)
    return token_schema


@router.get("/authorization", response_model=AccountBaseSchema)
async def authorization(
    decoded_jwt: Annotated[dict, Depends(decode_access_token)],
    db: Session = Depends(get_db),
) -> AccountBaseSchema:
    account_base_schema = controller.authorization(decoded_jwt, db)
    return account_base_schema
