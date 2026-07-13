from sqlmodel import SQLModel

class ClapCreate(SQLModel):
    post_id: int

class ClapResponse(SQLModel):
    id: int
    sayi: int
    kullanici_id: int
    post_id: int