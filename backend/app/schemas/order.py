from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.order import OrderStatus, PaymentStatus, PaymentMethod

class OrderItemBase(BaseModel):
    item_id: int
    quantity: float
    unit: str
    unit_price: float
    tax_rate: float = Field(default=0, ge=0, le=100)
    discount: float = Field(default=0, ge=0)
    notes: Optional[str] = None
    customization: Optional[Dict[str, Any]] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    total: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    amount: float
    payment_method: PaymentMethod
    reference: Optional[str] = None
    transaction_data: Optional[Dict[str, Any]] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    status: PaymentStatus

class Payment(PaymentBase):
    id: int
    order_id: int
    status: PaymentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    company_id: int
    store_id: int
    user_id: int
    status: OrderStatus = OrderStatus.PENDING
    subtotal: float
    tax: float = Field(default=0, ge=0)
    discount: float = Field(default=0, ge=0)
    total: float
    payment_status: PaymentStatus = PaymentStatus.PENDING
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None
    delivery_address: Optional[Dict[str, Any]] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(OrderBase):
    items: Optional[List[OrderItemCreate]] = None

class Order(OrderBase):
    id: int
    order_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItem] = []
    payments: List[Payment] = []

    class Config:
        from_attributes = True 