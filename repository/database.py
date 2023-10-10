from sqlmodel import SQLModel, create_engine
from models.Account import Account

engine = create_engine("sqlite://", echo=True)

