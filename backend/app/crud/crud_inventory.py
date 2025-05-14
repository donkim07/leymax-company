from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.inventory import Inventory, InventoryMovement
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryMovementCreate
)

class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    def get_store_inventory(
        self, db: Session, *, store_id: int, skip: int = 0, limit: int = 100
    ) -> List[Inventory]:
        return (
            db.query(Inventory)
            .filter(Inventory.store_id == store_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_item_inventory(
        self, db: Session, *, item_id: int, store_id: int
    ) -> Optional[Inventory]:
        return db.query(Inventory).filter(
            and_(
                Inventory.item_id == item_id,
                Inventory.store_id == store_id
            )
        ).first()

    def create_movement(
        self, db: Session, *, obj_in: InventoryMovementCreate
    ) -> InventoryMovement:
        db_obj = InventoryMovement(**obj_in.dict())
        db.add(db_obj)
        
        # Update inventory quantity
        inventory = db.query(Inventory).get(obj_in.inventory_id)
        if obj_in.movement_type in ["sale", "transfer_out", "adjustment_out"]:
            inventory.quantity -= obj_in.quantity
        else:
            inventory.quantity += obj_in.quantity
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def transfer_stock(
        self,
        db: Session,
        *,
        from_store_id: int,
        to_store_id: int,
        items: List[Dict[str, Any]]
    ) -> List[InventoryMovement]:
        movements = []
        for item in items:
            # Remove from source store
            from_inventory = self.get_item_inventory(
                db, item_id=item["item_id"], store_id=from_store_id
            )
            if not from_inventory or from_inventory.quantity < item["quantity"]:
                db.rollback()
                raise ValueError(f"Insufficient stock for item {item['item_id']}")
            
            out_movement = self.create_movement(
                db,
                obj_in=InventoryMovementCreate(
                    inventory_id=from_inventory.id,
                    movement_type="transfer_out",
                    quantity=item["quantity"],
                    unit=item["unit"],
                    notes=f"Transfer to store {to_store_id}"
                )
            )
            movements.append(out_movement)
            
            # Add to destination store
            to_inventory = self.get_item_inventory(
                db, item_id=item["item_id"], store_id=to_store_id
            )
            if not to_inventory:
                to_inventory = self.create(
                    db,
                    obj_in=InventoryCreate(
                        store_id=to_store_id,
                        item_id=item["item_id"],
                        quantity=0,
                        unit=item["unit"]
                    )
                )
            
            in_movement = self.create_movement(
                db,
                obj_in=InventoryMovementCreate(
                    inventory_id=to_inventory.id,
                    movement_type="transfer_in",
                    quantity=item["quantity"],
                    unit=item["unit"],
                    notes=f"Transfer from store {from_store_id}"
                )
            )
            movements.append(in_movement)
        
        return movements

crud_inventory = CRUDInventory(Inventory)
