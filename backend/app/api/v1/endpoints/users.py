from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[schemas.user.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve users.
    """
    if current_user.role == UserRole.ADMIN:
        users = crud.crud_user.get_multi(db, skip=skip, limit=limit)
    elif current_user.role == UserRole.MANAGER:
        # Managers can only see users in their store
        users = crud.crud_user.get_store_users(
            db, store_id=current_user.store_id, skip=skip, limit=limit
        )
    else:
        # Regular users can only see themselves
        users = [current_user]
    return users

@router.post("/", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new user.
    """
    # Check permissions
    if current_user.role != UserRole.ADMIN and user_in.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admins can create admin users"
        )
    
    if current_user.role == UserRole.MANAGER:
        # Managers can only create users for their store
        if user_in.store_id != current_user.store_id:
            raise HTTPException(
                status_code=403,
                detail="Can only create users for your store"
            )
        user_in.company_id = current_user.company_id
    
    user = crud.crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists"
        )
    return crud.crud_user.create(db=db, obj_in=user_in)

@router.put("/me", response_model=schemas.user.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserUpdate,
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update current user.
    """
    return crud.crud_user.update(db=db, db_obj=current_user, obj_in=user_in)

@router.get("/me", response_model=schemas.user.User)
def read_user_me(
    current_user: schemas.user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/{user_id}", response_model=schemas.user.User)
def read_user_by_id(
    user_id: int,
    current_user: schemas.user.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if current_user.role != UserRole.ADMIN:
        if user.company_id != current_user.company_id:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
    return user
