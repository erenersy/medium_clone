from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from data_models.user import User
from schemas.clap import ClapCreate, ClapResponse
from core.security import get_current_user
import crud.clap as clap_crud
import crud.post as post_crud

router = APIRouter(tags=["Clap"])


@router.post("/claplar", response_model=ClapResponse)
def clap_at(
    veri: ClapCreate,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, veri.post_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.durum != "published" and yazi.yazar_id != kullanici.id:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    return clap_crud.clap_at(session, veri, kullanici_id=kullanici.id)


@router.get("/yazilar/{yazi_id}/clap-sayisi")
def yazinin_clap_sayisi(yazi_id: int, session: Session = Depends(get_session)):
    toplam = clap_crud.yazinin_toplam_clap_sayisi(session, yazi_id)
    return {"post_id": yazi_id, "toplam_clap": toplam}