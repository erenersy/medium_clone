from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from schemas.user import UserCreate, UserResponse
from schemas.auth import LoginVerisi, TokenCifti, RefreshTokenVerisi
from core.security import sifre_dogrula, access_token_uret, refresh_token_uret, refresh_token_dogrula
import crud.user as user_crud

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def kayit_ol(veri: UserCreate, session: Session = Depends(get_session)):
    mevcut = user_crud.eposta_ile_kullanici_bul(session, veri.eposta)
    if mevcut:
        raise HTTPException(status_code=400, detail="Bu eposta zaten kayitli")
    return user_crud.kullanici_olustur(session, veri)


@router.post("/login", response_model=TokenCifti)
def giris_yap(veri: LoginVerisi, session: Session = Depends(get_session)):
    kullanici = user_crud.eposta_ile_kullanici_bul(session, veri.eposta)
    if not kullanici or not sifre_dogrula(veri.sifre, kullanici.sifre):
        raise HTTPException(status_code=401, detail="Eposta veya sifre hatali")
    return TokenCifti(
        access_token=access_token_uret(kullanici.id),
        refresh_token=refresh_token_uret(kullanici.id)
    )


@router.post("/refresh-token", response_model=TokenCifti)
def token_yenile(veri: RefreshTokenVerisi):
    kullanici_id = refresh_token_dogrula(veri.refresh_token)
    return TokenCifti(
        access_token=access_token_uret(kullanici_id),
        refresh_token=refresh_token_uret(kullanici_id)
    )