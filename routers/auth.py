from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from configs.db import get_session
from models.model import User
from utils.auth import create_access_token, verify_password

router = APIRouter(tags=["auth"])

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=Token)
def login_json(
    payload: LoginIn,                     # <-- FastAPI ahora busca JSON
    session: Session = Depends(get_session),
):
    stmt = select(User).where(User.email == payload.email)
    user = session.exec(stmt).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(401, "Credenciales incorrectas")
    token = create_access_token({ "sub": str(user.id),"name":str(user.name),"rol": user.rol.value })
    return {"access_token": token, "token_type": "bearer"}
