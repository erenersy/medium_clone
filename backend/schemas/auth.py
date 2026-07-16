from sqlmodel import SQLModel

class LoginVerisi(SQLModel):
    eposta: str
    sifre: str

class TokenCifti(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenVerisi(SQLModel):
    refresh_token: str