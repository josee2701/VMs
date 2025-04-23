
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configs.db import create_db_and_tables
from models.users import *
from routers.auth import router as auth_router
from routers.user import router as user_router
from routers.vm import router as vm_router

app = FastAPI()
# Orígenes que permites
origins = [
    "http://localhost:5173",
]

# Añade el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # <- aquí tus orígenes
    allow_credentials=True,           # si usas cookies/autenticación basada en credenciales
    allow_methods=["*"],              # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Authorization, Content-Type, …
)
# Incluimos el router de users
app.include_router(user_router)
# Incluimos el router de auth
app.include_router(auth_router)
# Incluimos el router de vms
app.include_router(vm_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()