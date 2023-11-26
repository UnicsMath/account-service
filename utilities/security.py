from datetime import datetime, timezone, timedelta
from os import getenv

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt as jose_jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import Annotated

load_dotenv(".env")

SECRET_KEY: str = getenv("JWT_SECRET_KEY")
ALGORITHM: str = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="authentication")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_hash(passcode: str) -> str:
    return pwd_context.hash(passcode)


def verify_hashes(plain_passcode: str, hashed_passcode: str) -> bool:
    return pwd_context.verify(plain_passcode, hashed_passcode)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jose_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(jwt: Annotated[str, Depends(OAUTH2_SCHEME)]) -> dict:
    try:
        return jose_jwt.decode(jwt, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception
