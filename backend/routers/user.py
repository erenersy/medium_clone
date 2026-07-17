from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from schemas.user import UserResponse, UserProfileResponse
import crud.user as user_crud
import crud.post as post_crud
import crud.follow as follow_crud
from schemas.post import PostResponse

router = APIRouter(prefix="/kullanicilar", tags=["User"])


@router.get("/{kullanici_id}", response_model=UserResponse)
def kullanici_bilgisi(kullanici_id: int, session: Session = Depends(get_session)):
    kullanici = user_crud.id_ile_kullanici_bul(session, kullanici_id)
    if not kullanici:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")
    return kullanici


@router.get("/{kullanici_id}/profil", response_model=UserProfileResponse)
def kullanici_profili(kullanici_id: int, session: Session = Depends(get_session)):
    kullanici = user_crud.id_ile_kullanici_bul(session, kullanici_id)
    if not kullanici:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")

    yazilar = post_crud.kullanicinin_yayinlanan_yazilarini_listele(session, kullanici_id)
    takipcileri = follow_crud.takipcileri_listele(session, kullanici_id)
    takip_ettikleri = follow_crud.takip_edilenleri_listele(session, kullanici_id)

    yazi_response_listesi = [
        PostResponse(
            id=y.id, baslik=y.baslik, icerik=y.icerik,
            durum=y.durum, yazar_id=y.yazar_id, yazar_isim=kullanici.isim
        )
        for y in yazilar
    ]

    return UserProfileResponse(
        id=kullanici.id,
        isim=kullanici.isim,
        eposta=kullanici.eposta,
        yazi_sayisi=len(yazilar),
        takipci_sayisi=len(takipcileri),
        takip_sayisi=len(takip_ettikleri),
        yazilar=yazi_response_listesi
    )