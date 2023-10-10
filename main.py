from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv

from schemas.account import Account

from repository.database import engine, SQLModel
from models.Account import Account as AccountModel
from sqlmodel import Session, select

load_dotenv(".env")

SECRET_KEY = getenv("JWT_SECRET_KEY")
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$4nwvJYSQkvK+F+K8955zLg$lLO71zm13Te+/h3pvD4lkIxw/eZ5ay3Czbu1aZsU7XU",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class AccountInDatabase(Account):
    hashed_password: str


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_database_and_tables():
    SQLModel.metadata.create_all(engine)


def create_account():
    account_1 = AccountModel(username="test1", email="test@test1.test", hashed_password=get_password_hash("test1"))
    account_2 = AccountModel(username="test2", email="test@test2.test", hashed_password=get_password_hash("test2"))
    account_3 = AccountModel(username="test3", email="test@test3.test", hashed_password=get_password_hash("test3"))

    with Session(engine) as session:
        session.add(account_1)
        session.add(account_2)
        session.add(account_3)

        session.commit()

        statement = select(AccountModel)
        accounts = session.exec(statement).all()
        for account in accounts:
            print(account)


def get_account_by_email(email: str):
    with Session(engine) as session:
        statement = select(AccountModel).where(AccountModel.email == email)
        return session.exec(statement).one()


def get_user(username: str):
    with Session(engine) as session:
        statement = select(AccountModel).where(AccountModel.username == username)
        return session.exec(statement).one()


app = FastAPI()
create_database_and_tables()
create_account()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str):
    user = get_account_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[Account, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=Account)
async def read_users_me(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
