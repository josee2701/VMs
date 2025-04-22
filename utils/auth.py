from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext

from configs.security import ALGORITHM, SECRET_KEY, get_token_expiry

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or get_token_expiry())
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
