from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class VMBase(SQLModel):
    name:   str  = Field(..., max_length=100)
    cores:  int  = Field(..., ge=1)
    ram:    int  = Field(..., ge=1, description="RAM en MB")
    disk:   int  = Field(..., ge=1, description="Disco en GB")
    os:     str  = Field(..., max_length=100)
    status: str  = Field(..., max_length=20, description="p.ej. running, stopped")

class VM(VMBase, table=True):
    id:          Optional[int]   = Field(default=None, primary_key=True)
    created_at:  datetime        = Field(default_factory=datetime.utcnow)
    updated_at:  datetime        = Field(default_factory=datetime.utcnow)

class VMCreate(VMBase):
    pass

class VMRead(VMBase):
    id:         int
    created_at: datetime
    updated_at: datetime

class VMUpdate(SQLModel):
    name:   Optional[str] = None
    cores:  Optional[int] = None
    ram:    Optional[int] = None
    disk:   Optional[int] = None
    os:     Optional[str] = None
    status: Optional[str] = None
