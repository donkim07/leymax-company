from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from datetime import datetime, timedelta
import logging

from app.core.config import settings
from app.core.security import create_access_token
from app.api import deps
from app.crud import crud_user, crud_company
from app.schemas import user as user_schemas
from app.schemas.register import CompanyRegistration
from app.models.user import UserRole, User
from app.schemas.auth import Token, LoginResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Constants for session management
SESSION_TOKEN_NAME = "session_token"
SESSION_EXPIRY_DAYS = 30

@router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    request: Request,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Log in with username and password
    """
    try:
        logger.debug(f"Login attempt for user: {form_data.username}")
        logger.debug(f"Request headers: {request.headers}")
        
        user = crud_user.authenticate(
            db, email=form_data.username, password=form_data.password
        )
        
        if not user:
            logger.debug(f"Authentication failed for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        elif not user.is_active:
            logger.debug(f"Inactive user attempt to login: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        logger.debug(f"User authenticated successfully: {user.email}")
        
        # Create token data - keep it minimal
        token_data = {
            "email": user.email
        }
        
        # Create user data for response
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "company_id": user.company_id,
            "store_id": user.store_id,
            "is_active": user.is_active
        }
        
        access_token = create_access_token(
            subject=user.id,
            data=token_data,
            expires_delta=timedelta(days=SESSION_EXPIRY_DAYS)
        )
        logger.debug(f"Created access token: {access_token[:10]}...")
        
        # Set cookie with access token
        expires = datetime.utcnow() + timedelta(days=SESSION_EXPIRY_DAYS)
        response.set_cookie(
            key=SESSION_TOKEN_NAME,
            value=access_token,
            httponly=True,
            # secure=True,  # Uncomment in production with HTTPS
            samesite="lax",  # Protect against CSRF
            expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            path="/"
        )
        logger.debug("Set session cookie")
        
        # Set Authorization header for API clients
        response.headers["Authorization"] = f"Bearer {access_token}"
        logger.debug("Set Authorization header")
        
        # Set CORS headers
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin", "http://localhost:3000")
        response.headers["Access-Control-Expose-Headers"] = "Authorization"
        
        logger.debug(f"Login successful for user: {user.email}")
        logger.debug(f"Response headers: {response.headers}")
        
        return {
            "user": user_data,
            "token": Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=SESSION_EXPIRY_DAYS * 24 * 60 * 60
            )
        }
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise

@router.post("/logout")
def logout(
    response: Response,
    session_token: Optional[str] = Cookie(None, alias=SESSION_TOKEN_NAME)
):
    """
    Log out current user
    """
    response.delete_cookie(
        key=SESSION_TOKEN_NAME,
        path="/"
    )
    return {"message": "Successfully logged out"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    *,
    db: Session = Depends(deps.get_db),
    registration: CompanyRegistration,
) -> Any:
    """
    Register a new company with the initial admin user.
    """
    # Check if user with email already exists
    user = crud_user.get_by_email(db, email=registration.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )
    
    # Create company with main store
    company = crud_company.create_with_store(
        db=db, 
        company_in=registration.company,
        store_in=registration.main_store
    )
    
    # Get the main store that was just created
    stores = crud_company.get_company_stores(db, company_id=company.id)
    main_store = stores[0]  # Should only be one store at this point
    
    # Create user
    user_data = user_schemas.UserCreate(
        email=registration.email,
        password=registration.password,
        first_name=registration.first_name,
        last_name=registration.last_name,
        company_id=company.id,
        store_id=main_store.id,
        phone=registration.phone,
        role=UserRole.ADMIN  # First user is always admin
    )
    
    user = crud_user.create(db=db, obj_in=user_data)
    
    return {
        "message": "Registration successful",
        "company": {
            "id": company.id,
            "name": company.name,
            "type": company.type
        },
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }

@router.get("/me", response_model=user_schemas.User)
def read_user_me(
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get current user.
    """
    return current_user
