from pydantic import BaseModel, EmailStr


class AccountBaseSchema(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None


class AccountInDatabaseSchema(AccountBaseSchema):
    hashed_password: str


class AccountSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True
