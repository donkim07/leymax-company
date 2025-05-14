from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()

@router.post("/", response_model=schemas.company.Company)
def create_company(
    *,
    db: Session = Depends(deps.get_db),
    company_in: schemas.company.CompanyCreate,
    current_user: schemas.user.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create new company.
    """
    company = crud.crud_company.get_by_name(db, name=company_in.name)
    if company:
        raise HTTPException(
            status_code=400,
            detail="A company with this name already exists."
        )
    return crud.crud_company.create(db=db, obj_in=company_in)

@router.get("/", response_model=List[schemas.company.Company])
def read_companies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.user.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Retrieve companies.
    """
    if current_user.role == UserRole.ADMIN:
        companies = crud.crud_company.get_multi(db, skip=skip, limit=limit)
    else:
        companies = [crud.crud_company.get(db, id=current_user.company_id)]
    return companies

@router.get("/{company_id}", response_model=schemas.company.CompanyWithStores)
def read_company(
    company_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get company by ID.
    """
    company = crud.crud_company.get_with_stores(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if current_user.role != UserRole.ADMIN and current_user.company_id != company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return company

@router.put("/{company_id}", response_model=schemas.company.Company)
def update_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    company_in: schemas.company.CompanyUpdate,
    current_user: schemas.user.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update company.
    """
    company = crud.crud_company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud.crud_company.update(db=db, db_obj=company, obj_in=company_in)

@router.post("/{company_id}/stores/", response_model=schemas.company.Store)
def create_store(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    store_in: schemas.company.StoreCreate,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new store for a company.
    """
    if current_user.role != UserRole.ADMIN and current_user.company_id != company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    store = crud.crud_store.get_by_code(db, code=store_in.code)
    if store:
        raise HTTPException(
            status_code=400,
            detail="A store with this code already exists."
        )
    return crud.crud_store.create(db=db, obj_in=store_in)

@router.get("/{company_id}/stores/", response_model=List[schemas.company.Store])
def read_stores(
    company_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve stores for a company.
    """
    if current_user.role != UserRole.ADMIN and current_user.company_id != company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.crud_store.get_company_stores(
        db=db, company_id=company_id, skip=skip, limit=limit
    )

@router.delete("/{company_id}", response_model=schemas.company.Company)
def delete_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    current_user = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Delete company.
    """
    company = crud.crud_company.get(db=db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
    company = crud.crud_company.remove(db=db, id=company_id)
    return company
