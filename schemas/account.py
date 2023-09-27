from pydantic import BaseModel


class Account(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None