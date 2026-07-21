from typing import List
from sqlmodel import Session, select
from data_models.tag import Tag
from data_models.post import Post
from data_models.post_tag_link import PostTagLink



def etiket_bul_veya_olustur(session: Session, isim: str) -> Tag:
    isim_normalize = isim.strip().lower()
    sorgu = select(Tag).where(Tag.isim == isim_normalize)
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

def tum_etiketleri_listele(session: Session) -> List[Tag]:
    sorgu = (
        select(Tag)
        .join(PostTagLink, PostTagLink.tag_id == Tag.id)
        .join(Post, Post.id == PostTagLink.post_id)
        .where(Post.durum == "published")
        .distinct()
    )
    return session.exec(sorgu).all()

def yazidan_etiket_cikar(session: Session, yazi: Post, etiket_isim: str) -> Post:
    etiket_isim_normalize = etiket_isim.strip().lower()
    yazi.etiketler = [e for e in yazi.etiketler if e.isim != etiket_isim_normalize]
    session.add(yazi)
    session.commit()
    session.refresh(yazi)
    return yazi