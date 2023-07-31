from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..schemas import UserCreate, UserUpdate, User, UserPartialUpdate, UserLogin, UserToken
from ..config.database import engine
from ..auth.crud import get_current_user
router = APIRouter(prefix="/users", tags=["Users"])

# Crear una sesión de base de datos
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for attr, value in user.model_dump().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.patch("/{user_id}", response_model=User)
def update_partial_user(user_id: int, user: UserPartialUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for attr, value in user.model_dump().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.get("/profile/current_user")
def get_profile(user=Depends(get_current_user), db: Session = Depends(get_db)):
    ## get users with donations list
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


  