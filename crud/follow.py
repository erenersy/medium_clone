from typing import List
from sqlmodel import Session, select
from data_models.follow import Follow


def takip_et(session: Session, takip_eden_id: int, takip_edilen_id: int) -> Follow:
    if takip_eden_id == takip_edilen_id:
        raise ValueError("Bir kullanici kendini takip edemez")

    sorgu = select(Follow).where(
        Follow.takip_eden_id == takip_eden_id,
        Follow.takip_edilen_id == takip_edilen_id
    )
    mevcut = session.exec(sorgu).first()
    if mevcut:
        return mevcut

    yeni_takip = Follow(
        takip_eden_id=takip_eden_id,
        takip_edilen_id=takip_edilen_id
    )
    session.add(yeni_takip)
    session.commit()
    session.refresh(yeni_takip)
    return yeni_takip


def takibi_birak(session: Session, takip_eden_id: int, takip_edilen_id: int) -> None:
    sorgu = select(Follow).where(
        Follow.takip_eden_id == takip_eden_id,
        Follow.takip_edilen_id == takip_edilen_id
    )
    kayit = session.exec(sorgu).first()
    if kayit:
        session.delete(kayit)
        session.commit()


def takipcileri_listele(session: Session, kullanici_id: int) -> List[Follow]:
    sorgu = select(Follow).where(Follow.takip_edilen_id == kullanici_id)
    return session.exec(sorgu).all()


def takip_edilenleri_listele(session: Session, kullanici_id: int) -> List[Follow]:
    sorgu = select(Follow).where(Follow.takip_eden_id == kullanici_id)
    return session.exec(sorgu).all()