from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator, Field
from datetime import datetime
from app.models.item import ItemType

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    company_id: int
    store_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    children: List['Category'] = []

    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    category_id: int
    unit_type: str
    cost_price: float = Field(ge=0)
    sell_price: float = Field(ge=0)
    tax_rate: float = Field(ge=0, le=100, default=0)
    reorder_point: int = Field(ge=0, default=0)
    company_id: int
    store_id: int
    is_active: bool = True
    metadata: Optional[Dict[str, Any]] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    current_stock: int = 0
    category: Optional[Category] = None

    class Config:
        from_attributes = True

class ItemWithInventory(Item):
    available_stock: int = 0
    reserved_stock: int = 0
    incoming_stock: int = 0
    outgoing_stock: int = 0

    @validator('available_stock', pre=True, always=True)
    def calculate_available_stock(cls, v, values):
        current = values.get('current_stock', 0)
        reserved = values.get('reserved_stock', 0)
        return current - reserved

# Prevent circular import issues with Category.children
Category.update_forward_refs()
