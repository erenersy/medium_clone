from typing import Optional, Literal
from sqlmodel import SQLModel

class PostCreate(SQLModel):
    baslik: str
    icerik: str

class PostResponse(SQLModel):
    id: int
    baslik: str
    icerik: str
    durum: str
    yazar_id: int

class PostUpdate(SQLModel):
    baslik: Optional[str] = None
    icerik: Optional[str] = None
    durum: Optional[Literal["draft", "published"]] = None