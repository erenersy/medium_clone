from typing import Optional
from sqlmodel import SQLModel
from schemas.post import PostResponse

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

class UserProfileResponse(SQLModel):
    id: int
    isim: str
    eposta: str
    yazi_sayisi: int
    takipci_sayisi: int
    takip_sayisi: int
    yazilar: list[PostResponse]