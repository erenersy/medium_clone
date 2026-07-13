from typing import List
from sqlmodel import Session, select
from data_models.tag import Tag
from data_models.post import Post


def etiket_bul_veya_olustur(session: Session, isim: str) -> Tag:
    sorgu = select(Tag).where(Tag.isim == isim)
    mevcut = session.exec(sorgu).first()
    if mevcut:
        return mevcut

    yeni_etiket = Tag(isim=isim)
    session.add(yeni_etiket)
    session.commit()
    session.refresh(yeni_etiket)
    return yeni_etiket


def yaziya_etiket_ekle(session: Session, yazi: Post, etiket_isimleri: List[str]) -> Post:
    for isim in etiket_isimleri:
        etiket = etiket_bul_veya_olustur(session, isim)
        if etiket not in yazi.etiketler:
            yazi.etiketler.append(etiket)
    session.add(yazi)
    session.commit()
    session.refresh(yazi)
    return yazi