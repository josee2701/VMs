# routers/user.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from configs.db import get_session
from models.model import User, UserCreate, UserRead, UserUpdate

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
