
from fastapi import FastAPI

from configs.db import create_db_and_tables
from models.model import *
from routers.user import router as user_router

app = FastAPI()

# Incluimos el router de users
app.include_router(user_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()