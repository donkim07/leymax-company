from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator
from app.models.user import UserRole

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    phone: Optional[str] = None
    address: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    role: UserRole
    company_id: int
    store_id: Optional[int] = None

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

    @validator('password')
    def validate_password(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    company_id: int
    store_id: Optional[int] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password_hash: str

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
