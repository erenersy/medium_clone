from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from backend.data_models.user import User
    from backend.data_models.post import Post

class Clap(SQLModel, table=True):
    __tablename__ = "claplar"

    id: Optional[int] = Field(default=None, primary_key=True)
    sayi: int = Field(default=1)   # bu kullanıcı bu yazıya kaç kez clap attı

    kullanici_id: int = Field(foreign_key="kullanicilar.id")
    kullanici: Optional["User"] = Relationship(back_populates="claplar")

    post_id: int = Field(foreign_key="yazilar.id")
    post: Optional["Post"] = Relationship(back_populates="claplar")