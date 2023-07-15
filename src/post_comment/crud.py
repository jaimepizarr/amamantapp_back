from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..schemas import (
    PostCommentCreate,
    PostCommentUpdate,
    PostComment,
    PostCommentPartialUpdate,
)
from ..config.database import engine

router = APIRouter(prefix="/post_comments", tags=["PostComments"])


# Crear una sesión de base de datos
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PostComment)
def create_post_comment(post_comment: PostCommentCreate, db: Session = Depends(get_db)):
    db_post_comment = models.PostComment(**post_comment.model_dump())
    db.add(db_post_comment)
    db.commit()
    db.refresh(db_post_comment)
    return db_post_comment


@router.get("/{post_comment_id}", response_model=PostComment)
def read_post_comment(post_comment_id: int, db: Session = Depends(get_db)):
    db_post_comment = (
        db.query(models.PostComment)
        .filter(models.PostComment.id == post_comment_id)
        .first()
    )
    if not db_post_comment:
        raise HTTPException(status_code=404, detail="PostComment not found")
    return db_post_comment


def update_general_post_comment(post_comment_id, post_comment, db):
    db_post_comment = (
        db.query(models.PostComment)
        .filter(models.PostComment.id == post_comment_id)
        .first()
    )
    if not db_post_comment:
        raise HTTPException(status_code=404, detail="PostComment not found")
    for attr, value in post_comment.model_dump().items():
        setattr(db_post_comment, attr, value)
    db.commit()
    db.refresh(db_post_comment)
    return db_post_comment


@router.put("/{post_comment_id}", response_model=PostComment)
def update_post_comment(
    post_comment_id: int, post_comment: PostCommentUpdate, db: Session = Depends(get_db)
):
    return update_general_post_comment(post_comment_id, post_comment, db)


@router.patch("/{post_comment_id}", response_model=PostComment)
def update_partial_post_comment(
    post_comment_id: int,
    post_comment: PostCommentPartialUpdate,
    db: Session = Depends(get_db),
):
    return update_general_post_comment(post_comment_id, post_comment, db)


@router.delete("/{post_comment_id}")
def delete_post_comment(post_comment_id: int, db: Session = Depends(get_db)):
    db_post_comment = (
        db.query(models.PostComment)
        .filter(models.PostComment.id == post_comment_id)
        .first()
    )
    if not db_post_comment:
        raise HTTPException(status_code=404, detail="PostComment not found")
    db.delete(db_post_comment)
    db.commit()
    return {"message": "PostComment deleted successfully"}
