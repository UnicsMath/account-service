from typing import Optional

from sqlmodel import Field, SQLModel


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(unique=True)
    hashed_password: Optional[str] = None
