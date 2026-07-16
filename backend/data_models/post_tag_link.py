from typing import Optional
from sqlmodel import SQLModel, Field

class PostTagLink(SQLModel, table=True):
    __tablename__ = "yazi_etiket_link"

    post_id: Optional[int] = Field(default=None, foreign_key="yazilar.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="etiketler.id", primary_key=True)