from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from data_models.user import User

class Follow(SQLModel, table=True):
    __tablename__ = "takipler"

    id: Optional[int] = Field(default=None, primary_key=True)

    takip_eden_id: int = Field(foreign_key="kullanicilar.id")
    takip_edilen_id: int = Field(foreign_key="kullanicilar.id")

    takip_eden: Optional["User"] = Relationship(
        back_populates="takip_ettikleri",
        sa_relationship_kwargs={"foreign_keys": "[Follow.takip_eden_id]"}
    )
    takip_edilen: Optional["User"] = Relationship(
        back_populates="takipcileri",
        sa_relationship_kwargs={"foreign_keys": "[Follow.takip_edilen_id]"}
    )