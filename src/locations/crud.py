from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..schemas import LocationCreate, LocationUpdate, Location, LocationPartialUpdate
from ..config.database import engine

router = APIRouter(prefix="/locations", tags=["Locations"])

# Crear una sesión de base de datos
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


# Operaciones CRUD para el modelo Location
@router.post("/", response_model=Location)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


@router.get("/{location_id}", response_model=Location)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@router.put("/{location_id}", response_model=Location)
def update_location(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    for attr, value in location.model_dump().items():
        setattr(db_location, attr, value)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.patch("/{location_id}", response_model=Location)
def update_partial_location(location_id: int, location: LocationPartialUpdate, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    for attr, value in location.model_dump().items():
        setattr(db_location, attr, value)
    db.commit()
    db.refresh(db_location)
    return db_location


@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted"}
