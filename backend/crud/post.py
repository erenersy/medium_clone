from typing import Optional, List
from sqlmodel import Session, select, func
from data_models.post import Post
from schemas.post import PostCreate, PostUpdate
from data_models.clap import Clap
from data_models.comment import Comment
from data_models.tag import Tag
from data_models.post_tag_link import PostTagLink
from sqlmodel import select


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


def yazi_sil(session: Session, yazi: Post):
    claplar = session.exec(select(Clap).where(Clap.post_id == yazi.id)).all()
    for clap in claplar:
        session.delete(clap)

    yorumlar = session.exec(select(Comment).where(Comment.post_id == yazi.id)).all()
    for yorum in yorumlar:
        session.delete(yorum)

    etiket_baglantilari = session.exec(select(PostTagLink).where(PostTagLink.post_id == yazi.id)).all()
    for baglanti in etiket_baglantilari:
        session.delete(baglanti)

    session.delete(yazi)
    session.commit()

def kullanicinin_yazilarini_listele(session: Session, yazar_id: int) -> List[Post]:
    sorgu = select(Post).where(Post.yazar_id == yazar_id)
    return session.exec(sorgu).all()

def kullanicinin_yayinlanan_yazilarini_listele(session: Session, yazar_id: int) -> List[Post]:
    sorgu = select(Post).where(Post.yazar_id == yazar_id, Post.durum == "published")
    return session.exec(sorgu).all()

def yazinin_kapak_resmini_guncelle(session: Session, yazi: Post, resim_yolu: str) -> Post:
    yazi.kapak_resmi = resim_yolu
    session.add(yazi)
    session.commit()
    session.refresh(yazi)
    return yazi

def en_cok_clap_alan_yazilar(session: Session, limit: int = 3) -> List[Post]:
    sorgu = (
        select(Post, func.sum(Clap.sayi).label("toplam"))
        .join(Clap, Clap.post_id == Post.id)
        .where(Post.durum == "published")
        .group_by(Post.id)
        .order_by(func.sum(Clap.sayi).desc())
        .limit(limit)
    )
    sonuclar = session.exec(sorgu).all()
    return [satir[0] for satir in sonuclar]

def etikete_gore_yayinlanmis_yazilari_listele(session: Session, etiket_isim: str) -> List[Post]:
    sorgu = (
        select(Post)
        .join(PostTagLink, PostTagLink.post_id == Post.id)
        .join(Tag, Tag.id == PostTagLink.tag_id)
        .where(Tag.isim == etiket_isim.strip().lower(), Post.durum == "published")
    )
    return session.exec(sorgu).all()