from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from data_models.user import User
from schemas.post import PostCreate, PostResponse, PostUpdate
from core.security import get_current_user
import crud.post as post_crud

router = APIRouter(prefix="/yazilar", tags=["Post"])


@router.post("", response_model=PostResponse)
def yazi_olustur(
    veri: PostCreate,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    return post_crud.yazi_olustur(session, veri, yazar_id=kullanici.id)


@router.get("", response_model=list[PostResponse])
def yayinlanmis_yazilar(session: Session = Depends(get_session)):
    return post_crud.yayinlanmis_yazilari_listele(session)


@router.get("/benim", response_model=list[PostResponse])
def kendi_yazilarim(
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    return post_crud.kullanicinin_yazilarini_listele(session, kullanici.id)


@router.get("/{yazi_id}", response_model=PostResponse)
def yazi_getir(yazi_id: int, session: Session = Depends(get_session)):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    return yazi


@router.put("/{yazi_id}", response_model=PostResponse)
def yazi_guncelle(
    yazi_id: int,
    veri: PostUpdate,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici.id:
        raise HTTPException(status_code=403, detail="Bu yaziyi guncelleme yetkiniz yok")
    return post_crud.yazi_guncelle(session, yazi, veri)


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