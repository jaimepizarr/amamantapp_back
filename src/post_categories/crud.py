from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..schemas import (
    PostCategoriesBase,
    PostCategoriesRetrieve
)
from ..config.database import engine

router = APIRouter(prefix="/post_categories", tags=["PostCategories"])

# Crear una sesión de base de datos
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=list[PostCategoriesRetrieve])
def get_all_post_categories(db: Session = Depends(get_db)):
    db_post_categories = db.query(models.PostCategory).all()
    if not db_post_categories:
        raise HTTPException(status_code=404, detail="No PostCategories created")
    return db_post_categories

@router.get("/{post_categories_id}", response_model=PostCategoriesRetrieve)
def read_post_categories(post_categories_id: int, db: Session = Depends(get_db)):
    db_post_categories = db.query(models.PostCategory).filter(models.PostCategory.id == post_categories_id).first()
    if not db_post_categories:
        raise HTTPException(status_code=404, detail="PostCategories not found")
    return db_post_categories

@router.post("/", response_model=PostCategoriesRetrieve)
def create_post_categories(post_categories: PostCategoriesBase, db: Session = Depends(get_db)):
    db_post_categories = models.PostCategory(**post_categories.model_dump())
    db.add(db_post_categories)
    db.commit()
    db.refresh(db_post_categories)
    return db_post_categories



