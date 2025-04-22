
from fastapi import FastAPI

from configs.db import create_db_and_tables
from models.model import *
from routers.auth import router as auth_router
from routers.user import router as user_router

app = FastAPI()

# Incluimos el router de users
app.include_router(user_router)
# Incluimos el router de auth
app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()