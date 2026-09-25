from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Student
from schemas import StudentCreate


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = Student(
        roll_no=student.roll_no,
        name=student.name,
        department=student.department,
        section=student.section
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.get("/")
def get_students(
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()

    return students