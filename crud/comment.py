from typing import List
from sqlmodel import Session, select
from data_models.comment import Comment
from schemas.comment import CommentCreate


def yorum_olustur(session: Session, veri: CommentCreate, yazan_id: int) -> Comment:
    yeni_yorum = Comment(
        icerik=veri.icerik,
        post_id=veri.post_id,
        yazan_id=yazan_id
    )
    session.add(yeni_yorum)
    session.commit()
    session.refresh(yeni_yorum)
    return yeni_yorum


def yazinin_yorumlarini_listele(session: Session, post_id: int) -> List[Comment]:
    sorgu = select(Comment).where(Comment.post_id == post_id)
    return session.exec(sorgu).all()


def yorum_bul(session: Session, yorum_id: int) -> Comment | None:
    return session.get(Comment, yorum_id)


def yorum_sil(session: Session, yorum: Comment) -> None:
    session.delete(yorum)
    session.commit()