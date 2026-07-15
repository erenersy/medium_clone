from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from data_models.user import User
from schemas.follow import FollowResponse
from core.security import get_current_user
import crud.follow as follow_crud
import crud.user as user_crud

router = APIRouter(tags=["Follow"])


@router.post("/takip/{takip_edilen_id}", response_model=FollowResponse)
def takip_et(
    takip_edilen_id: int,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    hedef = user_crud.id_ile_kullanici_bul(session, takip_edilen_id)
    if not hedef:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")
    try:
        return follow_crud.takip_et(session, takip_eden_id=kullanici.id, takip_edilen_id=takip_edilen_id)
    except ValueError as hata:
        raise HTTPException(status_code=400, detail=str(hata))


@router.delete("/takip/{takip_edilen_id}")
def takibi_birak(
    takip_edilen_id: int,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    follow_crud.takibi_birak(session, takip_eden_id=kullanici.id, takip_edilen_id=takip_edilen_id)
    return {"mesaj": "Takipten cikildi"}


@router.get("/kullanicilar/{kullanici_id}/takipcileri", response_model=list[FollowResponse])
def takipcileri_getir(kullanici_id: int, session: Session = Depends(get_session)):
    hedef = user_crud.id_ile_kullanici_bul(session, kullanici_id)
    if not hedef:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")
    return follow_crud.takipcileri_listele(session, kullanici_id)


@router.get("/kullanicilar/{kullanici_id}/takip-ettikleri", response_model=list[FollowResponse])
def takip_ettiklerini_getir(kullanici_id: int, session: Session = Depends(get_session)):
    hedef = user_crud.id_ile_kullanici_bul(session, kullanici_id)
    if not hedef:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")
    return follow_crud.takip_edilenleri_listele(session, kullanici_id)