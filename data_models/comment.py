from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from data_models.user import User
    from data_models.post import Post

class Comment(SQLModel, table=True):
    __tablename__ = "yorumlar"

    id: Optional[int] = Field(default=None, primary_key=True)
    icerik: str

    yazan_id: int = Field(foreign_key="kullanicilar.id")
    yazan: Optional["User"] = Relationship(back_populates="yorumlar")

    post_id: int = Field(foreign_key="yazilar.id")
    post: Optional["Post"] = Relationship(back_populates="yorumlar")