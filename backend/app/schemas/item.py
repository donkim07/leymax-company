from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.models.item import ItemType

class CategoryBase(BaseModel):
    company_id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    company_id: int
    name: str
    description: Optional[str] = None
    barcode: Optional[str] = None
    type: ItemType
    unit_type: str
    category_id: Optional[int] = None
    cost_price: float
    sell_price: float
    tax_rate: Optional[float] = 0.0
    image_url: Optional[str] = None
    reorder_point: Optional[float] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ItemWithInventory(Item):
    current_stock: Optional[float] = None
    available_stock: Optional[float] = None
