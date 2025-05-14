from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()

@router.get("/store/{store_id}", response_model=List[schemas.inventory.Inventory])
def read_store_inventory(
    store_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve store inventory.
    """
    store = crud.crud_store.get(db=db, id=store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not allowed to access this store's inventory")
    
    return crud.crud_inventory.get_store_inventory(
        db=db, store_id=store_id, skip=skip, limit=limit
    )

@router.post("/movement/", response_model=schemas.inventory.InventoryMovement)
def create_inventory_movement(
    *,
    db: Session = Depends(deps.get_db),
    movement_in: schemas.inventory.InventoryMovementCreate,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new inventory movement.
    """
    inventory = crud.crud_inventory.get(db=db, id=movement_in.inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    store = crud.crud_store.get(db=db, id=inventory.store_id)
    if store.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not allowed to modify this inventory")
    
    if current_user.role == UserRole.SALESPERSON and movement_in.movement_type not in ["sale"]:
        raise HTTPException(status_code=403, detail="Salesperson can only create sale movements")
    
    return crud.crud_inventory.create_movement(db=db, obj_in=movement_in)

@router.post("/transfer/", response_model=List[schemas.inventory.InventoryMovement])
def transfer_stock(
    *,
    db: Session = Depends(deps.get_db),
    transfer_in: schemas.inventory.StockTransferCreate,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Transfer stock between stores.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Verify stores belong to user's company
    from_store = crud.crud_store.get(db=db, id=transfer_in.from_store_id)
    to_store = crud.crud_store.get(db=db, id=transfer_in.to_store_id)
    
    if not from_store or not to_store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    if from_store.company_id != current_user.company_id or to_store.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not allowed to transfer between these stores")
    
    try:
        return crud.crud_inventory.transfer_stock(
            db=db,
            from_store_id=transfer_in.from_store_id,
            to_store_id=transfer_in.to_store_id,
            items=transfer_in.items
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
