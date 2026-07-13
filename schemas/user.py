from typing import Optional
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    isim: str
    eposta: str
    sifre: str

class UserResponse(SQLModel):
    id: int
    isim: str
    eposta: str

class UserUpdate(SQLModel):
    isim: Optional[str] = None
    eposta: Optional[str] = None
    sifre: Optional[str] = None