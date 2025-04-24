# routers/user.py
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from configs.db import get_session
from models.users import User, UserCreate, UserRead, UserUpdate
from utils.auth import hash_password
from utils.ws_broadcaster import manager

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=List[UserRead])
def list_users(*,session: Session = Depends(get_session),
):
    return session.exec(select(User)).all()

@router.get("/{user_id}", response_model=UserRead)
def get_user(*,user_id: int,session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    payload: UserCreate,
    background_tasks: BackgroundTasks,
    
    session: Session = Depends(get_session),
):
    # 1) Validación de unicidad
    if session.exec(select(User).where(User.email == payload.email)).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "USER_ALREADY_EXISTS",
                "message": "Ya existe un usuario con este email",
                "field": "email",
            },
        )

    # 2) Hash de contraseña
    pwd_hashed = hash_password(payload.password)
    user = User(
        name=payload.name,
        email=payload.email,
        rol=payload.rol,
        password=pwd_hashed,
    )

    # 3) Inserción con captura de errores
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DB_CONSTRAINT", "message": str(e.orig)},
        )
    
    # 4) Publicamos el evento en background para no bloquear
    background_tasks.add_task(
        manager.broadcast,
        {
            "event": "user_created",
            "user": UserRead.from_orm(user).dict(),
        },
    )

    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    user_id: int,
    payload: UserUpdate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "Usuario no encontrado", "field": "user_id"},
        )

    update_data = payload.dict(exclude_unset=True)
    if "email" in update_data:
        # comprueba unicidad email en otros registros
        exists = session.exec(
            select(User).where(User.email == update_data["email"], User.id != user_id)
        ).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "EMAIL_IN_USE", "message": "Este email está en uso", "field": "email"},
            )

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        session.commit()
        session.refresh(user)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DB_CONSTRAINT", "message": str(e.orig)},
        )
    # 🚀 emitimos evento “user_updated”
    background_tasks.add_task(
        manager.broadcast,
        {
            "event": "user_updated",
            "user": UserRead.from_orm(user).dict(),
        },
    )

    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    *,
    user_id: int,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "Usuario no encontrado", "field": "user_id"},
        )
    session.delete(user)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DB_CONSTRAINT", "message": str(e.orig)},
        )
    # 🚀 emitimos evento “user_deleted”
    background_tasks.add_task(
        manager.broadcast,
        {
            "event": "user_deleted",
            "user_id": user_id,
        },
    )
    return  # 204 no body
