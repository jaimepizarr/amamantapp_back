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

@router.post("/home")
def get_all_post_home(db: Session = Depends(get_db),  limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    db_post = db.query(models.PostHome).filter(
        models.PostHome.title.contains(search)
    ).limit(limit).offset(skip).all()
    if not db_post:
        raise HTTPException(status_code=404, detail="No Post created")
    return db_post

@router.post("/aprendemas")
def get_all_post_aprendemas(db: Session = Depends(get_db),  limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    db_post = db.query(models.PostAprendeMas).filter(
        models.PostAprendeMas.title.contains(search)
    ).limit(limit).offset(skip).all()
    if not db_post:
        raise HTTPException(status_code=404, detail="No Post created")
    return db_post

