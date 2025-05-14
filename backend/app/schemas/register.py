from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from app.models.user import UserRole
from app.models.company import CompanyType, StoreType

class StoreCreate(BaseModel):
    name: str
    type: StoreType
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class CompanyCreate(BaseModel):
    name: str
    type: CompanyType
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    logo_url: Optional[str] = None

class CompanyRegistration(BaseModel):
    """Complete registration schema for new companies with owner"""
    company: CompanyCreate
    main_store: StoreCreate
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
        
    @validator('main_store')
    def validate_store_type(cls, v):
        if v.type != StoreType.MAIN:
            raise ValueError("First store must be of type 'main'")
        return v 