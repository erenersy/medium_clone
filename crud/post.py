from typing import Optional, List
from sqlmodel import Session, select
from data_models.post import Post
from schemas.post import PostCreate, PostUpdate


def yazi_olustur(session: Session, veri: PostCreate, yazar_id: int) -> Post:
    yeni_yazi = Post(
        baslik=veri.baslik,
        icerik=veri.icerik,
        yazar_id=yazar_id
    )
    session.add(yeni_yazi)
    session.commit()
    session.refresh(yeni_yazi)
    return yeni_yazi


def yazi_bul(session: Session, yazi_id: int) -> Optional[Post]:
    return session.get(Post, yazi_id)


def yayinlanmis_yazilari_listele(session: Session) -> List[Post]:
    sorgu = select(Post).where(Post.durum == "published")
    return session.exec(sorgu).all()


def yazi_guncelle(session: Session, yazi: Post, veri: PostUpdate) -> Post:
    guncellenecek_alanlar = veri.model_dump(exclude_unset=True)
    for alan, deger in guncellenecek_alanlar.items():
        setattr(yazi, alan, deger)
    session.add(yazi)
    session.commit()
    session.refresh(yazi)
    return yazi


def yazi_sil(session: Session, yazi: Post) -> None:
    session.delete(yazi)
    session.commit()

def kullanicinin_yazilarini_listele(session: Session, yazar_id: int) -> List[Post]:
    sorgu = select(Post).where(Post.yazar_id == yazar_id)
    return session.exec(sorgu).all()