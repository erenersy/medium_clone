from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from data_models.user import User
from schemas.tag import TagResponse
from core.security import get_current_user
import crud.tag as tag_crud
import crud.post as post_crud
from schemas.post import PostResponse
from routers.post import _post_response_olustur

router = APIRouter(tags=["Tag"])


@router.post("/yazilar/{yazi_id}/etiketler", response_model=PostResponse)
def yaziya_etiket_ekle(
    yazi_id: int,
    etiket_isimleri: list[str],
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici.id:
        raise HTTPException(status_code=403, detail="Bu yaziya etiket ekleme yetkiniz yok")
    guncel_yazi = tag_crud.yaziya_etiket_ekle(session, yazi, etiket_isimleri)
    return _post_response_olustur(guncel_yazi, kullanici.isim)


@router.get("/etiketler", response_model=list[TagResponse])
def tum_etiketler(session: Session = Depends(get_session)):
    return tag_crud.tum_etiketleri_listele(session)

@router.delete("/yazilar/{yazi_id}/etiketler/{etiket_isim}", response_model=PostResponse)
def yaziden_etiket_sil(
    yazi_id: int,
    etiket_isim: str,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici.id:
        raise HTTPException(status_code=403, detail="Bu yaziyi guncelleme yetkiniz yok")
    guncel_yazi = tag_crud.yazidan_etiket_cikar(session, yazi, etiket_isim)
    return _post_response_olustur(guncel_yazi, kullanici.isim)