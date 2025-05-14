from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.models.inventory import MovementType

class InventoryBase(BaseModel):
    store_id: int
    item_id: int
    quantity: float
    unit: str

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    last_counted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class InventoryMovementBase(BaseModel):
    inventory_id: int
    movement_type: MovementType
    quantity: float
    unit: str
    batch_id: Optional[int] = None
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    notes: Optional[str] = None

class InventoryMovementCreate(InventoryMovementBase):
    pass

class InventoryMovement(InventoryMovementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class StockTransferBase(BaseModel):
    from_store_id: int
    to_store_id: int
    items: List[dict]  # [{item_id: int, quantity: float, unit: str}]
    notes: Optional[str] = None

class StockTransferCreate(StockTransferBase):
    pass

class StockTransfer(StockTransferBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
