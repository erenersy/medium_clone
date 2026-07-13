from sqlmodel import Session, select
from data_models.clap import Clap
from schemas.clap import ClapCreate


def clap_at(session: Session, veri: ClapCreate, kullanici_id: int) -> Clap:
    sorgu = select(Clap).where(
        Clap.kullanici_id == kullanici_id,
        Clap.post_id == veri.post_id
    )
    mevcut_clap = session.exec(sorgu).first()

    if mevcut_clap:
        mevcut_clap.sayi += 1
        session.add(mevcut_clap)
        session.commit()
        session.refresh(mevcut_clap)
        return mevcut_clap

    yeni_clap = Clap(
        kullanici_id=kullanici_id,
        post_id=veri.post_id,
        sayi=1
    )
    session.add(yeni_clap)
    session.commit()
    session.refresh(yeni_clap)
    return yeni_clap


def yazinin_toplam_clap_sayisi(session: Session, post_id: int) -> int:
    sorgu = select(Clap).where(Clap.post_id == post_id)
    claplar = session.exec(sorgu).all()
    return sum(c.sayi for c in claplar)