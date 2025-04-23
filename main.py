
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from configs.db import create_db_and_tables
from models.users import *
from routers.auth import router as auth_router
from routers.user import router as user_router
from routers.vm import router as vm_router
from utils.ws_broadcaster import manager, users_ws_endpoint

app = FastAPI()

# Orígenes que permites
origins = [
    "http://localhost:5173",
    "https://vms2.netlify.app"
]

# Configuracion para la base de datos
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,          
    allow_methods=["*"],             
    allow_headers=["*"],              
)

# Configuración de la API
# Incluimos el router de users
app.include_router(user_router)
# Incluimos el router de auth
app.include_router(auth_router)
# Incluimos el router de vms
app.include_router(vm_router)


# WebSocket endpoint
app.websocket("/ws/users")(users_ws_endpoint)


