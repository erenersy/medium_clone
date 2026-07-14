from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session

from db.session import veritabanini_olustur, get_session
from data_models.user import User
from data_models.post import Post
from data_models.comment import Comment
from data_models.clap import Clap
from data_models.follow import Follow
from data_models.tag import Tag
from data_models.post_tag_link import PostTagLink

from schemas.user import UserCreate, UserResponse
from schemas.post import PostCreate, PostResponse, PostUpdate
from schemas.comment import CommentCreate, CommentResponse
from schemas.clap import ClapCreate, ClapResponse
from schemas.follow import FollowResponse
from schemas.tag import TagCreate, TagResponse
from schemas.auth import LoginVerisi, TokenCifti, RefreshTokenVerisi
from core.security import (
    sifre_dogrula, access_token_uret, refresh_token_uret,
    get_current_user, refresh_token_dogrula
)

import crud.user as user_crud
import crud.post as post_crud
import crud.comment as comment_crud
import crud.clap as clap_crud
import crud.follow as follow_crud
import crud.tag as tag_crud

app = FastAPI(title="Medium Clone API")


@app.on_event("startup")
def startup():
    veritabanini_olustur()


# ----- AUTH -----

@app.post("/register", response_model=UserResponse)
def kayit_ol(veri: UserCreate, session: Session = Depends(get_session)):
    mevcut = user_crud.eposta_ile_kullanici_bul(session, veri.eposta)
    if mevcut:
        raise HTTPException(status_code=400, detail="Bu eposta zaten kayitli")
    return user_crud.kullanici_olustur(session, veri)


@app.post("/login", response_model=TokenCifti)
def giris_yap(veri: LoginVerisi, session: Session = Depends(get_session)):
    kullanici = user_crud.eposta_ile_kullanici_bul(session, veri.eposta)
    if not kullanici or not sifre_dogrula(veri.sifre, kullanici.sifre):
        raise HTTPException(status_code=401, detail="Eposta veya sifre hatali")
    return TokenCifti(
        access_token=access_token_uret(kullanici.id),
        refresh_token=refresh_token_uret(kullanici.id)
    )

@app.post("/refresh-token", response_model=TokenCifti)
def token_yenile(veri: RefreshTokenVerisi):
    kullanici_id = refresh_token_dogrula(veri.refresh_token)
    return TokenCifti(
        access_token=access_token_uret(kullanici_id),
        refresh_token=refresh_token_uret(kullanici_id)
    )

@app.get("/kullanicilar/{kullanici_id}", response_model=UserResponse)
def kullanici_profili(kullanici_id: int, session: Session = Depends(get_session)):
    kullanici = user_crud.id_ile_kullanici_bul(session, kullanici_id)
    if not kullanici:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")
    return kullanici

# ----- POST -----

@app.post("/yazilar", response_model=PostResponse)
def yazi_olustur(
    veri: PostCreate,
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    return post_crud.yazi_olustur(session, veri, yazar_id=kullanici_id)


@app.get("/yazilar", response_model=list[PostResponse])
def yayinlanmis_yazilar(session: Session = Depends(get_session)):
    return post_crud.yayinlanmis_yazilari_listele(session)

@app.get("/yazilarim", response_model=list[PostResponse])
def kendi_yazilarim(
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    return post_crud.kullanicinin_yazilarini_listele(session, kullanici_id)


@app.get("/yazilar/{yazi_id}", response_model=PostResponse)
def yazi_getir(yazi_id: int, session: Session = Depends(get_session)):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    return yazi


@app.put("/yazilar/{yazi_id}", response_model=PostResponse)
def yazi_guncelle(
    yazi_id: int,
    veri: PostUpdate,
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici_id:
        raise HTTPException(status_code=403, detail="Bu yaziyi guncelleme yetkiniz yok")
    return post_crud.yazi_guncelle(session, yazi, veri)


@app.delete("/yazilar/{yazi_id}")
def yazi_sil(
    yazi_id: int,
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici_id:
        raise HTTPException(status_code=403, detail="Bu yaziyi silme yetkiniz yok")
    post_crud.yazi_sil(session, yazi)
    return {"mesaj": "Yazi silindi"}

# ----- COMMENT -----

@app.post("/yorumlar", response_model=CommentResponse)
def yorum_olustur(
    veri: CommentCreate,
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, veri.post_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    return comment_crud.yorum_olustur(session, veri, yazan_id=kullanici_id)


@app.get("/yazilar/{yazi_id}/yorumlar", response_model=list[CommentResponse])
def yazinin_yorumlari(yazi_id: int, session: Session = Depends(get_session)):
    return comment_crud.yazinin_yorumlarini_listele(session, yazi_id)


@app.delete("/yorumlar/{yorum_id}")
def yorum_sil(
    yorum_id: int,
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    yorum = comment_crud.yorum_bul(session, yorum_id)
    if not yorum:
        raise HTTPException(status_code=404, detail="Yorum bulunamadi")
    if yorum.yazan_id != kullanici_id:
        raise HTTPException(status_code=403, detail="Bu yorumu silme yetkiniz yok")
    comment_crud.yorum_sil(session, yorum)
    return {"mesaj": "Yorum silindi"}

# ----- CLAP -----

@app.post("/claplar", response_model=ClapResponse)
def clap_at(
    veri: ClapCreate,
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, veri.post_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    return clap_crud.clap_at(session, veri, kullanici_id=kullanici_id)


@app.get("/yazilar/{yazi_id}/clap-sayisi")
def yazinin_clap_sayisi(yazi_id: int, session: Session = Depends(get_session)):
    toplam = clap_crud.yazinin_toplam_clap_sayisi(session, yazi_id)
    return {"post_id": yazi_id, "toplam_clap": toplam}

# ----- FOLLOW -----

@app.post("/takip/{takip_edilen_id}", response_model=FollowResponse)
def takip_et(
    takip_edilen_id: int,
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    hedef = user_crud.id_ile_kullanici_bul(session, takip_edilen_id)
    if not hedef:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")
    try:
        return follow_crud.takip_et(session, takip_eden_id=kullanici_id, takip_edilen_id=takip_edilen_id)
    except ValueError as hata:
        raise HTTPException(status_code=400, detail=str(hata))


@app.delete("/takip/{takip_edilen_id}")
def takibi_birak(
    takip_edilen_id: int,
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    follow_crud.takibi_birak(session, takip_eden_id=kullanici_id, takip_edilen_id=takip_edilen_id)
    return {"mesaj": "Takipten cikildi"}

@app.get("/kullanicilar/{kullanici_id}/takipcileri", response_model=list[FollowResponse])
def takipcileri_getir(kullanici_id: int, session: Session = Depends(get_session)):
    hedef = user_crud.id_ile_kullanici_bul(session, kullanici_id)
    if not hedef:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")
    return follow_crud.takipcileri_listele(session, kullanici_id)


@app.get("/kullanicilar/{kullanici_id}/takip-ettikleri", response_model=list[FollowResponse])
def takip_ettiklerini_getir(kullanici_id: int, session: Session = Depends(get_session)):
    hedef = user_crud.id_ile_kullanici_bul(session, kullanici_id)
    if not hedef:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")
    return follow_crud.takip_edilenleri_listele(session, kullanici_id)

# ----- TAG -----

@app.post("/yazilar/{yazi_id}/etiketler", response_model=PostResponse)
def yaziya_etiket_ekle(
    yazi_id: int,
    etiket_isimleri: list[str],
    session: Session = Depends(get_session),
    kullanici_id: int = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici_id:
        raise HTTPException(status_code=403, detail="Bu yaziya etiket ekleme yetkiniz yok")
    return tag_crud.yaziya_etiket_ekle(session, yazi, etiket_isimleri)

@app.get("/etiketler", response_model=list[TagResponse])
def tum_etiketler(session: Session = Depends(get_session)):
    return tag_crud.tum_etiketleri_listele(session)