from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    company_id: Optional[int] = None
    store_id: Optional[int] = None
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(UserBase):
    password: Optional[str] = None

    @validator('password')
    def validate_password(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: int  # user_id
    exp: int  # expiration time
    company_id: Optional[int] = None

# Password Reset Schemas
class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
