from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

# Base Models
class CompanyBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    tax_number: Optional[str] = None
    registration_number: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    modules: Optional[Dict[str, bool]] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Store Schemas
class StoreBase(BaseModel):
    company_id: int
    parent_store_id: Optional[int] = None
    name: str
    code: str
    store_type: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    is_active: bool = True
    settings: Optional[Dict[str, Any]] = None

    @validator('store_type')
    def validate_store_type(cls, v):
        if v not in ['main', 'sub']:
            raise ValueError('store_type must be either "main" or "sub"')
        return v

class StoreCreate(StoreBase):
    pass

class StoreUpdate(StoreBase):
    pass

class Store(StoreBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Response Models
class CompanyWithStores(Company):
    stores: List[Store] = []
