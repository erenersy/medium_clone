from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from data_models.post_tag_link import PostTagLink

if TYPE_CHECKING:
    from data_models.user import User
    from data_models.comment import Comment
    from data_models.clap import Clap
    from data_models.tag import Tag

class Post(SQLModel, table=True):
    __tablename__ = "yazilar"

    id: Optional[int] = Field(default=None, primary_key=True)
    baslik: str
    icerik: str
    durum: str = Field(default="draft")

    yazar_id: int = Field(foreign_key="kullanicilar.id")
    yazar: Optional["User"] = Relationship(back_populates="yazilar")
    yorumlar: List["Comment"] = Relationship(back_populates="post")
    claplar: List["Clap"] = Relationship(back_populates="post")
    etiketler: List["Tag"] = Relationship(back_populates="yazilar", link_model=PostTagLink)