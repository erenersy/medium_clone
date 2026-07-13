from sqlmodel import SQLModel

class TagCreate(SQLModel):
    isim: str

class TagResponse(SQLModel):
    id: int
    isim: str