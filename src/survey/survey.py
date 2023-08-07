
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from pydantic import ValidationError
from ..auth.crud import get_current_user
import json
from ..schemas import Survey
from .. import models 
from ..config.database import engine


router = APIRouter(prefix="/survey", tags=["Survey"])

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
@router.get("/")
def get_survey():
    survey = json.load(open("src/survey/questions.json"))
    return survey



@router.post("/")
def post_survey(survey:Survey,db: Session = Depends(get_db)):
   value_identifiers = {}
   data=survey.survey
   for index,question in enumerate(data['results']):
        value_identifier = question['results'][0]['valueIdentifier']
        value_identifiers[index+1] = value_identifier
   correct=	{ 1: "No", 2: "No", 3: "No", 4: "Si" }
   try:
        survey =models.Survey(survey=value_identifiers)
        db.add(survey)
        db.commit()
        db.refresh(survey)
        if value_identifiers == correct:
            return {"donant":True}
        return {"donant":False}
   except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    
    