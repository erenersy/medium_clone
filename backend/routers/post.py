from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from data_models.user import User
from schemas.post import PostCreate, PostResponse, PostUpdate
from core.security import get_current_user, get_current_user_optional
import crud.post as post_crud
from typing import Optional
from schemas.user import UserResponse
import crud.user as user_crud

router = APIRouter(prefix="/yazilar", tags=["Post"])

def _post_response_olustur(yazi, yazar_isim: str) -> PostResponse:
    return PostResponse(
        id=yazi.id, baslik=yazi.baslik, icerik=yazi.icerik,
        durum=yazi.durum, yazar_id=yazi.yazar_id, yazar_isim=yazar_isim
    )


@router.post("", response_model=PostResponse)
def yazi_olustur(veri: PostCreate, session: Session = Depends(get_session), kullanici: User = Depends(get_current_user)):
    yazi = post_crud.yazi_olustur(session, veri, yazar_id=kullanici.id)
    return _post_response_olustur(yazi, kullanici.isim)


@router.get("", response_model=list[PostResponse])
def yayinlanmis_yazilar(session: Session = Depends(get_session)):
    yazilar = post_crud.yayinlanmis_yazilari_listele(session)
    yazar_idleri = [y.yazar_id for y in yazilar]
    yazarlar = user_crud.id_listesiyle_kullanicilari_bul(session, yazar_idleri)
    return [_post_response_olustur(y, yazarlar[y.yazar_id].isim) for y in yazilar]


@router.get("/benim", response_model=list[PostResponse])
def kendi_yazilarim(session: Session = Depends(get_session), kullanici: User = Depends(get_current_user)):
    yazilar = post_crud.kullanicinin_yazilarini_listele(session, kullanici.id)
    return [_post_response_olustur(y, kullanici.isim) for y in yazilar]


@router.get("/{yazi_id}", response_model=PostResponse)
def yazi_getir(yazi_id: int, session: Session = Depends(get_session), kullanici: Optional[User] = Depends(get_current_user_optional)):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.durum != "published":
        if kullanici is None or yazi.yazar_id != kullanici.id:
            raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    yazar = user_crud.id_ile_kullanici_bul(session, yazi.yazar_id)
    return _post_response_olustur(yazi, yazar.isim)


@router.put("/{yazi_id}", response_model=PostResponse)
def yazi_guncelle(yazi_id: int, veri: PostUpdate, session: Session = Depends(get_session), kullanici: User = Depends(get_current_user)):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici.id:
        raise HTTPException(status_code=403, detail="Bu yaziyi guncelleme yetkiniz yok")
    guncel_yazi = post_crud.yazi_guncelle(session, yazi, veri)
    return _post_response_olustur(guncel_yazi, kullanici.isim)


@router.delete("/{yazi_id}")
def yazi_sil(
    yazi_id: int,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici.id:
        raise HTTPException(status_code=403, detail="Bu yaziyi silme yetkiniz yok")
    post_crud.yazi_sil(session, yazi)
    return {"mesaj": "Yazi silindi"}