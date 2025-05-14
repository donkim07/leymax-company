from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_course import crud_course
from app.schemas.academy import Course, CourseCreate, CourseUpdate, CourseSection, CourseSectionCreate

router = APIRouter()

@router.get("/", response_model=List[Course])
def read_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve courses for the current user's company.
    """
    courses = crud_course.get_multi_by_company(
        db=db, company_id=current_user.company_id, skip=skip, limit=limit
    )
    return courses

@router.post("/", response_model=Course)
def create_course(
    *,
    db: Session = Depends(deps.get_db),
    course_in: CourseCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Create new course.
    """
    course_in.company_id = current_user.company_id
    course = crud_course.create(db=db, obj_in=course_in)
    return course

@router.put("/{course_id}", response_model=Course)
def update_course(
    *,
    db: Session = Depends(deps.get_db),
    course_id: int,
    course_in: CourseUpdate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Update a course.
    """
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    course = crud_course.update(db=db, db_obj=course, obj_in=course_in)
    return course

@router.get("/{course_id}", response_model=Course)
def read_course(
    *,
    db: Session = Depends(deps.get_db),
    course_id: int,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get course by ID.
    """
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return course

@router.delete("/{course_id}")
def delete_course(
    *,
    db: Session = Depends(deps.get_db),
    course_id: int,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Delete a course.
    """
    course = crud_course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud_course.remove(db=db, id=course_id)
    return {"message": "Course deleted successfully"} 