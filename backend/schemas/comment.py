from sqlmodel import SQLModel

class CommentCreate(SQLModel):
    icerik: str
    post_id: int

class CommentResponse(SQLModel):
    id: int
    icerik: str
    yazan_id: int
    yazan_isim: str
    post_id: int
