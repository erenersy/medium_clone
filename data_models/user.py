from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from data_models.post import Post
    from data_models.comment import Comment
    from data_models.clap import Clap
    from data_models.follow import Follow

class User(SQLModel, table=True):
    __tablename__ = "kullanicilar"

    id: Optional[int] = Field(default=None, primary_key=True)
    isim: str
    eposta: str = Field(unique=True, index=True)
    sifre: str

    yazilar: List["Post"] = Relationship(back_populates="yazar")
    yorumlar: List["Comment"] = Relationship(back_populates="yazan")
    claplar: List["Clap"] = Relationship(back_populates="kullanici")
    takip_ettikleri: List["Follow"] = Relationship(
        back_populates="takip_eden",
        sa_relationship_kwargs={"foreign_keys": "[Follow.takip_eden_id]"}
    )
    takipcileri: List["Follow"] = Relationship(
        back_populates="takip_edilen",
        sa_relationship_kwargs={"foreign_keys": "[Follow.takip_edilen_id]"}
    )