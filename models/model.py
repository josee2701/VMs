
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    email: EmailStr

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None