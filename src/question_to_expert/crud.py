from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..schemas import QuestionToExpertCreate,QuestionToExpert
from .. import models
from ..config.database import engine

router = APIRouter(prefix="/question_to_expert", tags=["Question to expert"])


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@router.post("/",response_model=QuestionToExpert)
def create_question_to_expert(question_to_expert: QuestionToExpertCreate, db: Session = Depends(get_db)):
    db_question_to_expert = models.QuestionToExpert(**question_to_expert.model_dump())
    db.add(db_question_to_expert)
    db.commit()
    db.refresh(db_question_to_expert)
    return db_question_to_expert