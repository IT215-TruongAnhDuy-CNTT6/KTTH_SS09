from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

courses_db = [
    {"id": 1, "course_name": "FastAPI Masterclass", "duration_hours": 32, "price": 1500000, "status": "active", "created_at": "2026-07-01T02:00:00Z"},
    {"id": 2, "course_name": "NextJS Next-Level", "duration_hours": 45, "price": 1800000, "status": "active", "created_at": "2026-07-01T03:15:00Z"}
]

class CourseSchema(BaseModel):
    course_name: str = Field(min_length=5)
    duration_hours: int = Field(gt=0)
    price: int = Field(ge=0)

@app.get("/courses")
def get_courses():
    return {
        "statusCode": 200,
        "message": "Lấy danh sách khóa học thành công!",
        "data": courses_db,
        "error": None,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "path": "/courses"
    }

@app.post("/courses")
def add_course(course: CourseSchema):
    if next((c for c in courses_db if course.course_name.lower() == c.get("course_name").lower()), None):
        raise HTTPException(
            status_code=400,
            detail={
                "statusCode": 400,
                "message": "Lỗi: Tên khóa học này đã tồn tại trong danh mục đào tạo!",
                "data": None,
                "error": "ERR-EDU-01: Course name duplicates an existing record in memory array.",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "path": "/courses"
            }
        )
    new_course = {
        "id": len(courses_db) + 1,
        "course_name": course.course_name,
        "duration_hours": course.duration_hours,
        "price": course.price,
        "status": "active",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    courses_db.append(new_course)
    raise HTTPException(
        status_code=201,
        detail={
            "statusCode": 201,
            "message": "Tạo mới khóa học thành công!",
            "data": new_course,
            "error": None,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": "/courses"
        }
    )

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for c in courses_db:
        if course_id == c.get("course_id"):
            courses_db.remove(c)
            return {
                "statusCode": 200,
                "message": "Xóa khóa học thành công!",
                "data": c,
                "error": None,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "path": "/courses/{course_id}"
            }
    raise HTTPException(
        status_code=404,
        detail={
            "statusCode": 404,
            "message": "Lỗi: Không tìm thấy mã khóa học yêu cầu để xóa!",
            "data": None,
            "error": "ERR-EDU-02: Target course ID can not be found.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": "/courses/{course_id}"
        }
    )