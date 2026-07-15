from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from data_models.user import User
from schemas.comment import CommentCreate, CommentResponse
from core.security import get_current_user
import crud.comment as comment_crud
import crud.post as post_crud

router = APIRouter(tags=["Comment"])


@router.post("/yorumlar", response_model=CommentResponse)
def yorum_olustur(
    veri: CommentCreate,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, veri.post_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    return comment_crud.yorum_olustur(session, veri, yazan_id=kullanici.id)


@router.get("/yazilar/{yazi_id}/yorumlar", response_model=list[CommentResponse])
def yazinin_yorumlari(yazi_id: int, session: Session = Depends(get_session)):
    return comment_crud.yazinin_yorumlarini_listele(session, yazi_id)


@router.delete("/yorumlar/{yorum_id}")
def yorum_sil(
    yorum_id: int,
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    yorum = comment_crud.yorum_bul(session, yorum_id)
    if not yorum:
        raise HTTPException(status_code=404, detail="Yorum bulunamadi")
    if yorum.yazan_id != kullanici.id:
        raise HTTPException(status_code=403, detail="Bu yorumu silme yetkiniz yok")
    comment_crud.yorum_sil(session, yorum)
    return {"mesaj": "Yorum silindi"}