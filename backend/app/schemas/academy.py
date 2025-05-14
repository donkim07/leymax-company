from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.academy import CourseStatus, EnrollmentStatus

class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None
    video_url: Optional[str] = None
    duration: Optional[int] = None
    order: int
    is_preview: bool = False
    resources: Optional[Dict[str, Any]] = None

class LessonCreate(LessonBase):
    pass

class LessonUpdate(LessonBase):
    pass

class Lesson(LessonBase):
    id: int
    section_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CourseSectionBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int

class CourseSectionCreate(CourseSectionBase):
    lessons: Optional[List[LessonCreate]] = None

class CourseSectionUpdate(CourseSectionBase):
    lessons: Optional[List[LessonUpdate]] = None

class CourseSection(CourseSectionBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    lessons: List[Lesson] = []

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    company_id: int
    title: str
    description: Optional[str] = None
    price: float = Field(ge=0)
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    level: Optional[str] = None
    status: CourseStatus = CourseStatus.DRAFT
    is_featured: bool = False
    requirements: Optional[List[str]] = None
    what_you_learn: Optional[List[str]] = None

class CourseCreate(CourseBase):
    sections: Optional[List[CourseSectionCreate]] = None

class CourseUpdate(CourseBase):
    sections: Optional[List[CourseSectionUpdate]] = None

class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    sections: List[CourseSection] = []

    class Config:
        from_attributes = True

class CourseEnrollmentBase(BaseModel):
    course_id: int
    user_id: int
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE
    progress: float = Field(default=0, ge=0, le=100)

class CourseEnrollmentCreate(CourseEnrollmentBase):
    pass

class CourseEnrollmentUpdate(CourseEnrollmentBase):
    pass

class CourseEnrollment(CourseEnrollmentBase):
    id: int
    enrolled_at: datetime
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LessonProgressBase(BaseModel):
    enrollment_id: int
    lesson_id: int
    is_completed: bool = False
    progress: float = Field(default=0, ge=0, le=100)
    last_position: float = Field(default=0, ge=0)

class LessonProgressCreate(LessonProgressBase):
    pass

class LessonProgressUpdate(LessonProgressBase):
    pass

class LessonProgress(LessonProgressBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 