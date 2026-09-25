# from fastapi import FastAPI

# from database import engine, Base

# import models

# from routers import students, subjects, attendance


# app = FastAPI(
#     title="Smart Attendance Management System"
# )


# # Create database tables
# Base.metadata.create_all(bind=engine)


# # Include routers
# app.include_router(students.router)
# app.include_router(subjects.router)
# app.include_router(attendance.router)


# # Home API
# @app.get("/")
# def home():
#     return {
#         "message": "Smart Attendance Management System"
#     }
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import students
from routers import subjects
from routers import attendance

app = FastAPI()


app.include_router(students.router)
app.include_router(subjects.router)
app.include_router(attendance.router)


app.mount(
    "/frontend",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)


@app.get("/")
def home():
    return {
        "message": "Smart Attendance API"
    }