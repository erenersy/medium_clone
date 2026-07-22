from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import os
import shutil
import uuid
from fastapi import UploadFile, File
from db.session import get_session
from data_models.user import User
from schemas.post import PostCreate, PostResponse, PostUpdate
from core.security import get_current_user, get_current_user_optional
import crud.post as post_crud
from typing import Optional
from schemas.user import UserResponse
import crud.user as user_crud
from gtts import gTTS
import io
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/yazilar", tags=["Post"])

def _post_response_olustur(yazi, yazar_isim: str) -> PostResponse:
    return PostResponse(
        id=yazi.id, baslik=yazi.baslik, icerik=yazi.icerik,
        durum=yazi.durum, yazar_id=yazi.yazar_id, yazar_isim=yazar_isim,
        kapak_resmi=yazi.kapak_resmi,
        etiketler=[e.isim for e in yazi.etiketler]   # YENİ
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

@router.get("/one-cikanlar", response_model=list[PostResponse])
def one_cikan_yazilar(session: Session = Depends(get_session)):
    yazilar = post_crud.en_cok_clap_alan_yazilar(session, limit=3)
    yazar_idleri = [y.yazar_id for y in yazilar]
    yazarlar = user_crud.id_listesiyle_kullanicilari_bul(session, yazar_idleri)
    return [_post_response_olustur(y, yazarlar[y.yazar_id].isim) for y in yazilar]

@router.get("/etiket/{etiket_isim}", response_model=list[PostResponse])
def etikete_gore_yazilar(etiket_isim: str, session: Session = Depends(get_session)):
    yazilar = post_crud.etikete_gore_yayinlanmis_yazilari_listele(session, etiket_isim)
    yazar_idleri = [y.yazar_id for y in yazilar]
    yazarlar = user_crud.id_listesiyle_kullanicilari_bul(session, yazar_idleri)
    return [_post_response_olustur(y, yazarlar[y.yazar_id].isim) for y in yazilar]

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

IZIN_VERILEN_UZANTILAR = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
UPLOAD_KLASORU = "uploads"

@router.post("/{yazi_id}/kapak-resmi", response_model=PostResponse)
def kapak_resmi_yukle(
    yazi_id: int,
    dosya: UploadFile = File(...),
    session: Session = Depends(get_session),
    kullanici: User = Depends(get_current_user)
):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")
    if yazi.yazar_id != kullanici.id:
        raise HTTPException(status_code=403, detail="Bu yaziyi guncelleme yetkiniz yok")

    uzanti = os.path.splitext(dosya.filename)[1].lower()
    if uzanti not in IZIN_VERILEN_UZANTILAR:
        raise HTTPException(status_code=400, detail="Sadece jpg, png, webp, gif dosyalari kabul edilir")

    os.makedirs(UPLOAD_KLASORU, exist_ok=True)
    dosya_adi = f"{uuid.uuid4().hex}{uzanti}"
    kayit_yolu = os.path.join(UPLOAD_KLASORU, dosya_adi)

    with open(kayit_yolu, "wb") as hedef:
        shutil.copyfileobj(dosya.file, hedef)

    guncel_yazi = post_crud.yazinin_kapak_resmini_guncelle(session, yazi, f"/uploads/{dosya_adi}")
    return _post_response_olustur(guncel_yazi, kullanici.isim)

@router.get("/{yazi_id}/sesli-oku")
def yaziyi_sesli_oku(yazi_id: int, dil: str = "tr", session: Session = Depends(get_session)):
    yazi = post_crud.yazi_bul(session, yazi_id)
    if not yazi:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi")

    gecici = f'<div>{yazi.icerik}</div>'
    import re
    temiz_metin = re.sub(r'<[^>]+>', ' ', gecici)

    metin = f"{yazi.baslik}. {temiz_metin}"
    ses = gTTS(text=metin, lang=dil)

    ses_verisi = io.BytesIO()
    ses.write_to_fp(ses_verisi)
    ses_verisi.seek(0)

    return StreamingResponse(ses_verisi, media_type="audio/mpeg")