from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from data_models.user import User
from schemas.comment import CommentCreate, CommentResponse
from core.security import get_current_user
import crud.comment as comment_crud
import crud.post as post_crud
import crud.user as user_crud

router = APIRouter(tags=["Comment"])

def _comment_response_olustur(yorum, yazan_isim: str) -> CommentResponse:
    return CommentResponse(
        id=yorum.id, icerik=yorum.icerik,
        yazan_id=yorum.yazan_id, yazan_isim=yazan_isim, post_id=yorum.post_id
    )

@router.post("/yorumlar", response_model=CommentResponse)
def yorum_olustur(veri: CommentCreate, session: Session = Depends(get_session), kullanici: User = Depends(get_current_user)):
    yazi = post_crud.yazi_bul(session, veri.post_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.durum != "published" and yazi.yazar_id != kullanici.id:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    yorum = comment_crud.yorum_olustur(session, veri, yazan_id=kullanici.id)
    return _comment_response_olustur(yorum, kullanici.isim)

@router.get("/yazilar/{yazi_id}/yorumlar", response_model=list[CommentResponse])
def yazinin_yorumlari(yazi_id: int, session: Session = Depends(get_session)):
    yorumlar = comment_crud.yazinin_yorumlarini_listele(session, yazi_id)
    yazan_idleri = [y.yazan_id for y in yorumlar]
    yazanlar = user_crud.id_listesiyle_kullanicilari_bul(session, yazan_idleri)
    return [_comment_response_olustur(y, yazanlar[y.yazan_id].isim) for y in yorumlar]


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