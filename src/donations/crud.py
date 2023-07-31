from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import ValidationError
from sqlalchemy.orm import Session
from .. import models 
from ..schemas import DonationCreate, DonationUpdate, Donation
from ..auth.crud import get_current_user
from ..config.database import engine

router = APIRouter(prefix="/donations", tags=["Donations"])

# Crear una sesión de base de datos
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


# Operaciones CRUD para el modelo Location

@router.post("/", response_model=Donation)
def create_donation(donation: DonationCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        db_donation = models.Donation(**donation.model_dump())
        db_donation.user_id = user.id
        db.add(db_donation)
        db.commit()
        db.refresh(db_donation)
        return db_donation
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())


@router.get("/{donation_id}", response_model=Donation)
def read_donation(donation_id: int, db: Session = Depends(get_db)):
    db_donation = db.query(models.Donation).filter(models.Donation.id == donation_id).first()
    if not db_donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return db_donation

@router.put("/{donation_id}", response_model=Donation)
def update_donation(donation_id: int, donation: DonationUpdate, db: Session = Depends(get_db)):
    db_donation = db.query(models.Donation).filter(models.Donation.id == donation_id).first()
    if not db_donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    for attr, value in donation.model_dump().items():
        setattr(db_donation, attr, value)
    db.commit()
    db.refresh(db_donation)
    return db_donation

@router.delete("/{donation_id}")
def delete_donation(donation_id: int, db: Session = Depends(get_db)):
    db_donation = db.query(models.Donation).filter(models.Donation.id == donation_id).first()
    if not db_donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    db.delete(db_donation)
    db.commit()
    return {"message": "Donation deleted successfully"}