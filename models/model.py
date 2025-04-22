
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class RoleEnum(str, Enum):
    administrator = "administrator"
    client        = "cliente"

class UserBase(SQLModel):
    name: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    email: EmailStr
    rol: RoleEnum = Field(default=RoleEnum.client)
    
    def __str__(self):
        return f"{self.name} - {self.email} - {self.rol}"
    
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