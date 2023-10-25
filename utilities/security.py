from datetime import datetime, timezone, timedelta
from os import getenv
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv(".env")

SECRET_KEY: str = getenv("JWT_SECRET_KEY")
ALGORITHM: str = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_hash(passcode: str) -> str:
    return pwd_context.hash(passcode)


def verify_hashes(plain_passcode: str, hashed_passcode: str) -> bool:
    return pwd_context.verify(plain_passcode, hashed_passcode)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
