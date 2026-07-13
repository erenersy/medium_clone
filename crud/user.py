from sqlmodel import Session, select
from data_models.user import User
from schemas.user import UserCreate
from core.security import sifre_hashle


def kullanici_olustur(session: Session, veri: UserCreate) -> User:
    yeni_kullanici = User(
        isim=veri.isim,
        eposta=veri.eposta,
        sifre=sifre_hashle(veri.sifre)
    )
    session.add(yeni_kullanici)
    session.commit()
    session.refresh(yeni_kullanici)
    return yeni_kullanici


def eposta_ile_kullanici_bul(session: Session, eposta: str) -> User | None:
    sorgu = select(User).where(User.eposta == eposta)
    return session.exec(sorgu).first()


def id_ile_kullanici_bul(session: Session, kullanici_id: int) -> User | None:
    return session.get(User, kullanici_id)