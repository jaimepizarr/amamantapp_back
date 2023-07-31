from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..config.database import engine

router = APIRouter(prefix="/post", tags=["Post"])

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
@router.get("/home/posts/{section}")
def get_all_post_home(db: Session = Depends(get_db), limit: int = 10, page: int = 1, section: str = ''):
    skip = (page - 1) * limit
    db_post = db.query(models.PostHome).filter(
        models.PostHome.section.has(name=section)  
    ).limit(limit).offset(skip).all()
    if not db_post:
        raise HTTPException(status_code=404, detail="No Post created")

    return db_post

@router.get("/home/{post_id}")
def get_post_home(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.PostHome).filter(models.PostHome.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.get("/aprendemas/posts/{section}")
def get_all_post_aprendemas(db: Session = Depends(get_db), section: str = '', limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    db_post = db.query(models.PostAprendeMas).filter(
        models.PostAprendeMas.section.has(name=section)  
    ).limit(limit).offset(skip).all()
    if not db_post:
        raise HTTPException(status_code=404, detail="No Post created")

    return db_post

@router.get("/aprendemas/{post_id}")
def get_post_aprendemas(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.PostAprendeMas).filter(models.PostAprendeMas.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post