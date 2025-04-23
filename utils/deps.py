import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from configs.db import get_session
from configs.security import ALGORITHM, SECRET_KEY
from models.users import RoleEnum, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar credenciales",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_rol = payload.get("rol")
    except jwt.PyJWTError:
        raise cred_exc

    user = session.get(User, int(user_id))
    if not user or user.rol.value != token_rol:
        raise cred_exc
    return user

def require_administrator(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.rol != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )
    return current_user
