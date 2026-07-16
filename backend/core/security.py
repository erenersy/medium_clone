from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os
from sqlmodel import Session
from db.session import get_session
from data_models.user import User

load_dotenv()

def _env_zorunlu(anahtar: str) -> str:
    deger = os.getenv(anahtar)
    if not deger:
        raise RuntimeError(f".env dosyasinda '{anahtar}' degeri eksik veya bos")
    return deger

SECRET_KEY = _env_zorunlu("SECRET_KEY")
ALGORITHM = _env_zorunlu("ALGORITHM")

try:
    ACCESS_TOKEN_SURESI_DAKIKA = int(_env_zorunlu("ACCESS_TOKEN_SURESI_DAKIKA"))
    REFRESH_TOKEN_SURESI_GUN = int(_env_zorunlu("REFRESH_TOKEN_SURESI_GUN"))
except ValueError:
    raise RuntimeError("ACCESS_TOKEN_SURESI_DAKIKA ve REFRESH_TOKEN_SURESI_GUN sayisal bir deger olmali")

security = HTTPBearer()

# Passlib'i tamamen devre dışı bırakıp doğrudan ham bcrypt motorunu kullanıyoruz
def sifre_hashle(sifre: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(sifre.encode('utf-8'), salt).decode('utf-8')

def sifre_dogrula(duz_sifre: str, hash_sifre: str) -> bool:
    try:
        return bcrypt.checkpw(duz_sifre.encode('utf-8'), hash_sifre.encode('utf-8'))
    except Exception:
        return False

def token_uret(kullanici_id: int, token_tipi: str, sure: timedelta) -> str:
    son_kullanma = datetime.now(timezone.utc) + sure
    payload = {
        "sub": str(kullanici_id),
        "type": token_tipi,
        "exp": son_kullanma
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def access_token_uret(kullanici_id: int) -> str:
    return token_uret(kullanici_id, "access", timedelta(minutes=ACCESS_TOKEN_SURESI_DAKIKA))

def refresh_token_uret(kullanici_id: int) -> str:
    return token_uret(kullanici_id, "refresh", timedelta(days=REFRESH_TOKEN_SURESI_GUN))

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials
    hata = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Gecersiz veya suresi dolmus token"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise hata
        kullanici_id = payload.get("sub")
        if kullanici_id is None:
            raise hata
        kullanici = session.get(User, int(kullanici_id))
        if kullanici is None:
            raise hata
        return kullanici
    except JWTError:
        raise hata

def refresh_token_dogrula(token: str, session: Session) -> User:
    hata = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Gecersiz veya suresi dolmus refresh token"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise hata
        kullanici_id = payload.get("sub")
        if kullanici_id is None:
            raise hata
        kullanici = session.get(User, int(kullanici_id))
        if kullanici is None:
            raise hata
        return kullanici
    except JWTError:
        raise hata

security_optional = HTTPBearer(auto_error=False)

def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security_optional),
    session: Session = Depends(get_session)
) -> Optional[User]:
    if credentials is None:
        return None
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        kullanici_id = payload.get("sub")
        if kullanici_id is None:
            return None
        return session.get(User, int(kullanici_id))
    except JWTError:
        return None