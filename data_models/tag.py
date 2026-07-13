from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from data_models.post_tag_link import PostTagLink

if TYPE_CHECKING:
    from data_models.post import Post

class Tag(SQLModel, table=True):
    __tablename__ = "etiketler"

    id: Optional[int] = Field(default=None, primary_key=True)
    isim: str = Field(unique=True, index=True)

    yazilar: List["Post"] = Relationship(back_populates="etiketler", link_model=PostTagLink)