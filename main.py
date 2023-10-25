from fastapi import FastAPI

from routers.account_router import router

from models import account_model
from repository.database import engine

account_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
