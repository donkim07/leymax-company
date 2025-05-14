from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any, List
from datetime import timedelta

from app.core.config import settings
from app.core import security
from app.api import deps
from app.crud import crud_user
from app.schemas import user as user_schemas

router = APIRouter()

@router.post("/login", response_model=user_schemas.Token)
async def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, user.company_id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=user_schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )
    return crud_user.create(db=db, obj_in=user_in)

@router.get("/me", response_model=user_schemas.User)
def read_user_me(
    current_user: user_schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=user_schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schemas.UserUpdate,
    current_user: user_schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    return crud_user.update(db, db_obj=current_user, obj_in=user_in)

@router.post("/password-reset", response_model=dict)
def request_password_reset(
    email_in: user_schemas.PasswordReset,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Password recovery
    """
    user = crud_user.get_by_email(db, email=email_in.email)
    if user:
        # Send password reset email
        pass
    return {"msg": "If a user with that email exists, a password reset link has been sent."}
