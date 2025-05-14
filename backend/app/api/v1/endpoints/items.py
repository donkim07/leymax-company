from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()

@router.post("/categories/", response_model=schemas.item.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.item.CategoryCreate,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """Create new category."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if current_user.company_id != category_in.company_id:
        raise HTTPException(status_code=403, detail="Not allowed to create category for other companies")
    
    category = crud.crud_category.get_by_name(
        db, name=category_in.name, company_id=category_in.company_id
    )
    if category:
        raise HTTPException(
            status_code=400,
            detail="Category with this name already exists"
        )
    return crud.crud_category.create(db=db, obj_in=category_in)

@router.get("/categories/", response_model=List[schemas.item.Category])
def read_categories(
    company_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """Retrieve categories."""
    if current_user.company_id != company_id:
        raise HTTPException(status_code=403, detail="Not allowed to access other companies' categories")
    return crud.crud_category.get_company_categories(
        db=db, company_id=company_id, skip=skip, limit=limit
    )

@router.post("/", response_model=schemas.item.Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.item.ItemCreate,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """Create new item."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if current_user.company_id != item_in.company_id:
        raise HTTPException(status_code=403, detail="Not allowed to create items for other companies")
    
    if item_in.barcode:
        item = crud.crud_item.get_by_barcode(db, barcode=item_in.barcode)
        if item:
            raise HTTPException(
                status_code=400,
                detail="Item with this barcode already exists"
            )
    
    item = crud.crud_item.get_by_name(
        db, name=item_in.name, company_id=item_in.company_id
    )
    if item:
        raise HTTPException(
            status_code=400,
            detail="Item with this name already exists in your company"
        )
    return crud.crud_item.create(db=db, obj_in=item_in)

@router.get("/", response_model=List[schemas.item.ItemWithInventory])
def read_items(
    company_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """Retrieve items."""
    if current_user.company_id != company_id:
        raise HTTPException(status_code=403, detail="Not allowed to access other companies' items")
    return crud.crud_item.get_company_items(
        db=db, company_id=company_id, skip=skip, limit=limit
    )

@router.get("/{item_id}", response_model=schemas.item.ItemWithInventory)
def read_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """Get item by ID."""
    item = crud.crud_item.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not allowed to access this item")
    return item
