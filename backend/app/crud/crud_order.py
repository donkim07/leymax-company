from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate

class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_multi_by_company(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(Order)
            .filter(Order.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_store(
        self, db: Session, *, store_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(Order)
            .filter(Order.store_id == store_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: OrderCreate) -> Order:
        obj_in_data = jsonable_encoder(obj_in, exclude={"items"})
        db_obj = Order(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Create order items
        if obj_in.items:
            for item in obj_in.items:
                item_data = jsonable_encoder(item)
                db_item = OrderItem(**item_data, order_id=db_obj.id)
                db.add(db_item)
            db.commit()
            db.refresh(db_obj)

        return db_obj

    def update(
        self, db: Session, *, db_obj: Order, obj_in: OrderUpdate
    ) -> Order:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        # Update order items if provided
        if "items" in update_data:
            # Remove existing items
            db.query(OrderItem).filter(OrderItem.order_id == db_obj.id).delete()
            
            # Add new items
            for item in update_data["items"]:
                db_item = OrderItem(**item, order_id=db_obj.id)
                db.add(db_item)
            
            del update_data["items"]

        # Update order fields
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_order = CRUDOrder(Order) 