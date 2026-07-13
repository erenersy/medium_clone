from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_SURESI_DAKIKA = int(os.getenv("ACCESS_TOKEN_SURESI_DAKIKA"))
REFRESH_TOKEN_SURESI_GUN = int(os.getenv("REFRESH_TOKEN_SURESI_GUN"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def sifre_hashle(sifre: str) -> str:
    return pwd_context.hash(sifre)


def sifre_dogrula(duz_sifre: str, hash_sifre: str) -> bool:
    return pwd_context.verify(duz_sifre, hash_sifre)


def token_uret(kullanici_id: int, token_tipi: str, sure: timedelta) -> str:
    son_kullanma = datetime.now(timezone.utc) + sure
    payload = {
        "sub": str(kullanici_id),
        "type": token_tipi,   # "access" ya da "refresh"
        "exp": son_kullanma
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def access_token_uret(kullanici_id: int) -> str:
    return token_uret(kullanici_id, "access", timedelta(minutes=ACCESS_TOKEN_SURESI_DAKIKA))


def refresh_token_uret(kullanici_id: int) -> str:
    return token_uret(kullanici_id, "refresh", timedelta(days=REFRESH_TOKEN_SURESI_GUN))


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
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
        return int(kullanici_id)
    except JWTError:
        raise hata