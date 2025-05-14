from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from app.models.company import CompanyType, StoreType

# Store Schemas
class StoreBase(BaseModel):
    name: str
    type: StoreType
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class StoreCreate(StoreBase):
    company_id: Optional[int] = None
    parent_store_id: Optional[int] = None

class StoreUpdate(StoreBase):
    pass

class Store(StoreBase):
    id: int
    company_id: int
    parent_store_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Company Schemas
class CompanyBase(BaseModel):
    name: str
    type: CompanyType
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    logo_url: Optional[str] = None
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
    stores: List[Store] = []

    class Config:
        from_attributes = True

# Response Models
class CompanyWithStores(Company):
    stores: List[Store] = []
