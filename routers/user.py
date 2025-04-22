# routers/user.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from configs.db import get_session
from models.model import User, UserCreate, UserRead, UserUpdate
from utils.auth import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    *,
    payload: UserCreate,
    session: Session = Depends(get_session),
):
    # construimos el User a partir del payload
    user = User(**payload.dict())
     # 1) hashea antes de instanciar el User
    pwd_hashed = hash_password(payload.password)
    user = User(
        name=payload.name,
        email=payload.email,
        rol=payload.rol,
        password=pwd_hashed,      # guardas el hash, no el texto
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserRead)
def read_user(
    *,
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    return user

@router.get("/", response_model=List[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()
    return users

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    user_id: int,
    payload: UserUpdate,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    update_data = payload.dict(exclude_unset=True)
     # si viene password, hashealo
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for field, value in update_data.items():
        setattr(user, field, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    *,
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    session.delete(user)
    session.commit()
    # FastAPI entiende que 204 no retornará body
    return
