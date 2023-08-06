from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..schemas import UserCreate, UserUpdate, User, UserPartialUpdate, UserLogin, UserToken
from ..config.database import engine
from ..auth.crud import get_current_user, get_password_hash 
from ..config.firestore import add_document, update_document, delete_document
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
        if (attr != "profile_picture" and value != None):
            if (type(value) == "string" and not len(value.strip())):
                continue
            if (attr == "password"):
                if (value.strip() != ""):
                    value = get_password_hash(value)
                else:
                    continue
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
        if (attr != "profile_picture" and value != None):
            if (type(value) == "string" and not len(value.strip())):
                continue
            if (attr == "password"):
                if (value.strip() != ""):
                    value = get_password_hash(value)
                else:
                    continue
            setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    updtObj = {"uid": str(user_id), "nombre":db_user.nombre, "apellido":db_user.apellido}
    if (user.model_dump().get("profile_picture") != None):
        updtObj["profile_picture"] = user.model_dump().get("profile_picture")
    doc_updt = update_document("users",str(user_id), updtObj)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    document_deleted = delete_document("users", str(user_id))
    if( document_deleted["success"]):
        return {"message": "User deleted completely successfully"}
    else:
        return {"message": "User deleted successfully from db but not from firebase."+document_deleted["message"]}


@router.get("/profile/current_user")
def get_profile(user=Depends(get_current_user), db: Session = Depends(get_db)):
    ## get users with donations list
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


  