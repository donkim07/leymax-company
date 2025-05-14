from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.academy import Course, CourseSection, Lesson
from app.schemas.academy import CourseCreate, CourseUpdate

class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):
    def get_multi_by_company(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        return (
            db.query(Course)
            .filter(Course.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: CourseCreate) -> Course:
        obj_in_data = jsonable_encoder(obj_in, exclude={"sections"})
        db_obj = Course(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Create course sections if provided
        if obj_in.sections:
            for section in obj_in.sections:
                section_data = jsonable_encoder(section, exclude={"lessons"})
                db_section = CourseSection(**section_data, course_id=db_obj.id)
                db.add(db_section)
                db.commit()
                db.refresh(db_section)

                # Create lessons for each section if provided
                if section.lessons:
                    for lesson in section.lessons:
                        lesson_data = jsonable_encoder(lesson)
                        db_lesson = Lesson(**lesson_data, section_id=db_section.id)
                        db.add(db_lesson)
                    db.commit()

        return db_obj

    def update(
        self, db: Session, *, db_obj: Course, obj_in: CourseUpdate
    ) -> Course:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        # Update sections if provided
        if "sections" in update_data:
            # Remove existing sections and their lessons
            for section in db_obj.sections:
                db.query(Lesson).filter(Lesson.section_id == section.id).delete()
            db.query(CourseSection).filter(CourseSection.course_id == db_obj.id).delete()
            
            # Add new sections and lessons
            for section in update_data["sections"]:
                section_data = jsonable_encoder(section, exclude={"lessons"})
                db_section = CourseSection(**section_data, course_id=db_obj.id)
                db.add(db_section)
                db.commit()
                db.refresh(db_section)

                if section.lessons:
                    for lesson in section.lessons:
                        lesson_data = jsonable_encoder(lesson)
                        db_lesson = Lesson(**lesson_data, section_id=db_section.id)
                        db.add(db_lesson)
                    db.commit()
            
            del update_data["sections"]

        # Update course fields
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_course = CRUDCourse(Course) 