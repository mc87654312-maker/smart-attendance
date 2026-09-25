from pydantic import BaseModel
from datetime import date


class StudentCreate(BaseModel):
    roll_no: str
    name: str
    department: str
    section: str


class SubjectCreate(BaseModel):
    name: str
    department: str
    section: str


class AttendanceCreate(BaseModel):
    student_id: int
    subject_id: int
    date: date
    status: str