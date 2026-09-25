from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Attendance, Student, Subject
from schemas import AttendanceCreate


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# POST - Create attendance
@router.post("/")
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):

    # Check student
    student = db.query(Student).filter(
        Student.id == attendance.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check subject
    subject = db.query(Subject).filter(
        Subject.id == attendance.subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    # Check duplicate attendance
    existing = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.subject_id == attendance.subject_id,
        Attendance.date == attendance.date
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Attendance already exists for this student, subject and date"
        )

    # Create attendance
    new_attendance = Attendance(
        student_id=attendance.student_id,
        subject_id=attendance.subject_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


# GET - View all attendance
@router.get("/")
def get_attendance(
    db: Session = Depends(get_db)
):

    attendance = db.query(Attendance).all()

    return attendance




# GET - Attendance report for a student
@router.get("/report/{student_id}")
def attendance_report(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Check if student exists
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Get attendance records for this student
    records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    # Total classes
    total_classes = len(records)

    # Count present
    present = sum(
        1 for record in records
        if record.status == "Present"
    )

    # Count absent
    absent = sum(
        1 for record in records
        if record.status == "Absent"
    )

    # Calculate percentage
    if total_classes > 0:
        attendance_percentage = (
            present / total_classes
        ) * 100
    else:
        attendance_percentage = 0

    return {
        "student_id": student_id,
        "total_classes": total_classes,
        "present": present,
        "absent": absent,
        "attendance_percentage": attendance_percentage
    }

# GET - Attendance analysis
@router.get("/analysis/{student_id}")
def attendance_analysis(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Check student
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Get attendance records
    records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    total_classes = len(records)

    present = sum(
        1 for record in records
        if record.status == "Present"
    )

    absent = sum(
        1 for record in records
        if record.status == "Absent"
    )

    # Calculate percentage
    if total_classes > 0:
        percentage = (present / total_classes) * 100
    else:
        percentage = 0

    # Analyze attendance
    if percentage >= 75:
        message = "Attendance is good."
    elif percentage >= 60:
        message = "Attendance is below 75%. Student should attend more classes."
    else:
        message = "Attendance is very low. Student needs immediate attention."

    return {
        "student_id": student_id,
        "total_classes": total_classes,
        "present": present,
        "absent": absent,
        "attendance_percentage": percentage,
        "analysis": message
    }