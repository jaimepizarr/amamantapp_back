from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..models import AppSuggestions
from ..schemas import AppSuggestions, AppSuggestionsCreate, AppSuggestionsUpdate
from ..config.database import engine

router = APIRouter(prefix="/app_suggestions", tags=["App Suggestions"])

# Crear una sesión de base de datos
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AppSuggestions)
def create_app_suggestion(app_suggestion: AppSuggestionsCreate, db: Session = Depends(get_db)):
    db_app_suggestion = AppSuggestions(**app_suggestion.model_dump())
    db.add(db_app_suggestion)
    db.commit()
    db.refresh(db_app_suggestion)
    return db_app_suggestion

