from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Subject
from schemas import SubjectCreate


router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db)
):
    new_subject = Subject(
        name=subject.name,
        department=subject.department,
        section=subject.section
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject


@router.get("/")
def get_subjects(
    db: Session = Depends(get_db)
):
    subjects = db.query(Subject).all()

    return subjects