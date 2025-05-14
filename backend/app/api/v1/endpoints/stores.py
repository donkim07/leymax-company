from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_store import crud_store
from app.schemas.company import Store, StoreCreate, StoreUpdate

router = APIRouter()

@router.get("/", response_model=List[Store])
def read_stores(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve stores for the current user's company.
    """
    stores = crud_store.get_multi_by_company(
        db=db, company_id=current_user.company_id, skip=skip, limit=limit
    )
    return stores

@router.post("/", response_model=Store)
def create_store(
    *,
    db: Session = Depends(deps.get_db),
    store_in: StoreCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Create new store.
    """
    store = crud_store.create(db=db, obj_in=store_in)
    return store

@router.put("/{store_id}", response_model=Store)
def update_store(
    *,
    db: Session = Depends(deps.get_db),
    store_id: int,
    store_in: StoreUpdate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Update a store.
    """
    store = crud_store.get(db=db, id=store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    store = crud_store.update(db=db, db_obj=store, obj_in=store_in)
    return store

@router.get("/{store_id}", response_model=Store)
def read_store(
    *,
    db: Session = Depends(deps.get_db),
    store_id: int,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get store by ID.
    """
    store = crud_store.get(db=db, id=store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return store

@router.delete("/{store_id}")
def delete_store(
    *,
    db: Session = Depends(deps.get_db),
    store_id: int,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Delete a store.
    """
    store = crud_store.get(db=db, id=store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud_store.remove(db=db, id=store_id)
    return {"message": "Store deleted successfully"} 