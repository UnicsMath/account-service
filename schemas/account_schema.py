from pydantic import BaseModel, EmailStr


class AccountBaseSchema(BaseModel):
    username: str
    email: EmailStr | None = None


class AccountInDatabaseSchema(AccountBaseSchema):
    hashed_passcode: str


class AccountSchema(BaseModel):
    id: int

    class Config:
        from_attribute = True
