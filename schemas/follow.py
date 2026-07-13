from sqlmodel import SQLModel

class FollowCreate(SQLModel):
    takip_edilen_id: int

class FollowResponse(SQLModel):
    id: int
    takip_eden_id: int
    takip_edilen_id: int