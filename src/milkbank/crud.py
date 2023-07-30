from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..schemas import MilkBankCreate, MilkBankUpdate, MilkBank, MilkBankPartialUpdate
from ..config.database import engine

router = APIRouter(prefix="/milkbanks", tags=["MilkBanks"])

# Crear una sesión de base de datos
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MilkBank)
def create_milkbank(milkbank: MilkBankCreate, db: Session = Depends(get_db)):
    db_milkbank = models.MilkBank(**milkbank.model_dump())
    db.add(db_milkbank)
    db.commit()
    db.refresh(db_milkbank)
    return db_milkbank

@router.get("/", response_model=list[MilkBank])
def get_all_milkbank(db: Session = Depends(get_db),  limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    db_milkbanks = db.query(models.MilkBank).filter(
        models.MilkBank.name.contains(search)
    ).limit(limit).offset(skip).all()
    if not db_milkbanks:
        raise HTTPException(status_code=404, detail="No Milkbank created")
    return db_milkbanks

@router.get("/{milkbank_id}", response_model=MilkBank)
def read_milkbank(milkbank_id: int, db: Session = Depends(get_db)):
    db_milkbank = db.query(models.MilkBank).filter(models.MilkBank.id == milkbank_id).first()
    if not db_milkbank:
        raise HTTPException(status_code=404, detail="MilkBank not found")
    return db_milkbank

def update_general_milkbank(milkbank_id, milkbank, db):
    db_milkbank = db.query(models.MilkBank).filter(models.MilkBank.id == milkbank_id).first()
    if not db_milkbank:
        raise HTTPException(status_code=404, detail="MilkBank not found")
    for attr, value in milkbank.model_dump().items():
        setattr(db_milkbank, attr, value)
    db.commit()
    db.refresh(db_milkbank)
    return db_milkbank

@router.put("/{milkbank_id}", response_model=MilkBank)
def update_milkbank(milkbank_id: int, milkbank: MilkBankUpdate, db: Session = Depends(get_db)):
    return update_general_milkbank(milkbank_id, milkbank, db)

@router.patch("/{milkbank_id}", response_model=MilkBank)
def update_partial_milkbank(milkbank_id: int, milkbank: MilkBankPartialUpdate, db: Session = Depends(get_db)):
    return update_general_milkbank(milkbank_id, milkbank, db)

@router.delete("/{milkbank_id}")
def delete_milkbank(milkbank_id: int, db: Session = Depends(get_db)):
    db_milkbank = db.query(models.MilkBank).filter(models.MilkBank.id == milkbank_id).first()
    if not db_milkbank:
        raise HTTPException(status_code=404, detail="MilkBank not found")
    db.delete(db_milkbank)
    db.commit()
    return {"message": f"MilkBank with id {milkbank_id} deleted successfully"}